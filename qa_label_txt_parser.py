import json
import logging
from pathlib import Path
from typing import List, Dict

logging.basicConfig(format="%(levelname)s - %(message)s",)
_logger = logging.getLogger()
_logger.setLevel(logging.ERROR)


def get_value(line: str) -> str:
    assert isinstance(line, str)
    try:
        start = line.index("{{") + 2
        end = line.index("}}")
    except:
        raise Exception(f"`{line}` does not satisfy expected format")
    value = line[start:end].strip()
    return value


def qa_section_parser(qa_section: List) -> Dict:
    # store parsed data
    qa_section_data: Dict = {}
    # store options
    option_lst: List = []
    # store correct answer index
    correct_ans: List = []
    qn = ""

    for line in qa_section:
        line: str
        if line.startswith("!"):
            break
        elif line.startswith("---------"):
            q_type = get_value(line)
        elif line.startswith("<Q-sub>"):
            q_sub = get_value(line)
            if q_sub == "None":
                q_sub = None
            else:
                # TODO: Get substitution
                sub = ""
                qn = sub
        elif line.startswith("<A-sub>"):
            a_sub = get_value(line)
            if a_sub == "None":
                a_sub = None
            else:
                # TODO: Get substitution
                sub = []
                option_lst += sub
        elif line.startswith("<ANS>"):
            ans = get_value(line)
            if ans == "+":
                pass
            else:
                ans_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
                for char in ans.upper():
                    if char in ans_map:
                        correct_ans.append(ans_map[char])
        else:
            if not q_sub and "?" in line:
                qn = line.strip()
            elif q_sub and "?" in line:
                _logger.error("Question line detected while <Q-sub> is not None.")
            else:
                if line:
                    option_lst.append(line)

    if ans == "+":
        for index, option in enumerate(option_lst):
            if option.startswith("+"):
                correct_ans.append(index)
                option_lst[index] = option.strip("+").strip()

    qa_section_data["q_type"] = q_type
    qa_section_data["correct_ans"] = correct_ans
    qa_section_data["qn"] = qn
    qa_section_data["options"] = option_lst

    return qa_section_data


def vid_section_parser(vid_section: List) -> Dict:
    # store parsed data
    vid_section_data: Dict = {}
    # store the indexes where a vid_section starts
    qa_section_indexes = []
    # traverse thru vid_section line by line
    for index, line in enumerate(vid_section):
        if line.startswith("--------------------"):
            qa_section_indexes.append(index)

    num_qa_sections = len(qa_section_indexes)
    _logger.info(f"Number of QA sections found: {num_qa_sections}")

    vid_info_section: List = vid_section[: qa_section_indexes[0]]
    for line in vid_info_section:
        if line.startswith("~~~~~~~~~~~~~~~~~~~~ "):
            _logger.debug("video section")
            filename = line.strip("~").strip()
            vid_section_data["filename"] = filename
            _logger.debug(f"video: {filename}")
        elif line.startswith("<PERSPECTIVE>"):
            perspective = get_value(line)
            if perspective == "":
                _logger.error(f"Missing required <PERSPECTIVE> for {filename}")
            else:
                vid_section_data["perspective"] = perspective
        elif line.startswith("<RE_TRIM>"):
            re_trim_ts = get_value(line)
            if re_trim_ts == "START_TS, END_TS":
                _logger.debug("no re-trimming needed")
                re_trim_ts = None
            else:
                pass
                # TODO: validation
            vid_section_data["re_trim_ts"] = re_trim_ts

        elif line.startswith("<CRITICAL_POINT>"):
            critical_ts = get_value(line)
            if critical_ts == "TS":
                _logger.debug("no CRITICAL POINT")
                critical_ts = None
            else:
                # TODO: store value
                # TODO: time validation
                pass
            vid_section_data["critical_ts"] = critical_ts

    # create qa list
    qa_list: List[Dict] = []
    # split a video section into qa sections
    for index, section_start in enumerate(qa_section_indexes):
        if index < num_qa_sections - 1:
            qa_section: List = vid_section[
                section_start : qa_section_indexes[index + 1]
            ]
        else:
            qa_section: List = vid_section[section_start:]

        qa_list.append(qa_section_parser(qa_section))

    vid_section_data["qa_list"] = qa_list

    return vid_section_data


def parse_qa_label_txt(txt_fp: str, writeToJson=False) -> List[Dict]:
    # store parsed result
    qa_label_lst: List[Dict] = []
    # ensure txt file path is valid
    txt_fp = Path(txt_fp)
    assert txt_fp.is_file()

    # reas txt as a list of lines
    with txt_fp.open() as f:
        lines: List = f.readlines()

    lines: List = list(map(lambda x: x.strip("\n"), lines))

    # store the indexes where a vid_section starts
    vid_section_indexes = []

    # look for video sections
    for index, line in enumerate(lines):
        line: str = line.strip()
        if line.startswith("~~~~~~~~~~~~~~~~~~~~ "):
            vid_section_indexes.append(index)

    num_video_sections = len(vid_section_indexes)
    _logger.info(f"Number of video sections found: {num_video_sections}")

    # split the whole txt file into video sections
    for index, section_start in enumerate(vid_section_indexes):
        if index < num_video_sections - 1:
            vid_section: List = lines[section_start : vid_section_indexes[index + 1]]
        else:
            vid_section: List = lines[section_start:]

        qa_label_lst.append(vid_section_parser(vid_section))

    if writeToJson:
        export_fp: Path = txt_fp.parent / "qa.json"
        with export_fp.open(mode="w") as f:
            f.write(json.dumps(qa_label_lst, indent=4))
            _logger.debug(f"Successfully exported: {export_fp}")

    return qa_label_lst


if __name__ == "__main__":
    parse_qa_label_txt("example/qa_label_template.txt", writeToJson=True)
