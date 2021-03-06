# EasyLabel

## QA Label `.txt` File Convention

### Example
```
~~~~~~~~~~~~~~~~~~~~ video_file_name ~~~~~~~~~~~~~~~~~~~~
<LENGTH=1.74s>
<DIM=(W)1920 x (H)1080>
<PERSPECTIVE>: {{ 3 }}             // use [1/3]
<RE_TRIM>: {{ START_TS, END_TS }}  // 00:00.000, 00:00.000
<CRITICAL_POINT>: {{ TS }}         // 00:00.000

-----------------{{ d }}          // this is the question type
<Q-sub>: {{ None }}               // question substitution
<A-sub>: {{ None }}               // options substitution
<ANS>: {{ + }}                    // use + as default or [A|B|C|D], support multiple correct answer
What the colour of the truck?     // if no Q-sub is used, question is asked with a "?" question mark
red                               // followed by options
+black                            // use "+" to mark correct answer(s)
white
pink
grey

-----------------{{ p }}
<Q-sub>: {{ 2 }}
<A-sub>: {{ 3 }}
<ANS>: {{ + }}
+green

-----------------{{ r }}
<Q-sub>: {{ 3 }}
<A-sub>: {{ 5 }}
<ANS>: {{ A }}
green

!-----------------{{ i }}  // skipped question
<Q-sub>: {{ None }}
<A-sub>: {{ None }}
<ANS>: {{ + }}
What the colour of the truck?
red
+black
white
pink
grey

~~~~~~~~~~~~~~~~~~~~ another_video ~~~~~~~~~~~~~~~~~~~~
<LENGTH=1.74s>
<DIM=(W)1920 x (H)1080>
<PERSPECTIVE>: {{ 1 }}              // use [1/3]
<RE_TRIM>: {{ START_TS, END_TS }}  // 00:00.000, 00:00.000
<CRITICAL_POINT>: {{ TS }}         // 00:00.000

--------------------{{  }} // Q Type: use [1-6]|[d|e|p|r|c|i]
<Q-sub>: {{ None }}
<A-sub>: {{ None }}
<ANS>: {{ + }}             // use + as default or [A|B|C|D]
```
