For some random reason, I attempted to use my spare time to write something on Kindle.
What you dream is light, what you see is night.Amazon designed the Kindle to be used for reading books, not for writing,the Kindle's text input function is only suitable for notes, obviously not for writing a novel.

Why develop a text editor on  Kindle instead of on smartphone:
1.The smartphone screen is small, and the keyboard is much smaller, it's fine for writing quick messages, but not for composing long story.
2.Outside, especially in direct sunlight, the smartphone screen is hazy.
3.The smartphone's standby time isn't very long.it will become pretty heated if you write on your smartphone for two hours.
4.There are so many apps running on smartphone， and there are so many news and message alerts that it's impossible to focus on writing.

Major functions of the n31_kte:
1.edit text file
2.paint image
3.send email
4.download text file from cloud
5.adjust background light, screenshot, turn on/off WiFi, calculator, flashlight...


Kindle Text Editor v2.18 English version for KO2、KO3:
https://drive.google.com/file/d/1VNM6WeCGyG-nBjbJxZKib9lt_ovWyjBA/view?usp=sharing

Kindle Text Editor v2.18 English version for  for KPW3、KPW4、KV、KO:
https://drive.google.com/file/d/17E4vk8_y32tC7Fw4i9loquG7jJn5e5JF/view?usp=sharing
------------------------------------------------------------------------------------------------------------------
Kindle Text Editor v2.18 Chinese version for KO2、KO3: (include Chinese pinyin input Lib, need more ram to run)：
https://drive.google.com/file/d/1EEFpbvFwwQpC8fdK75wVkoYEsGND7qPJ/view?usp=sharing

Kindle Text Editor v2.18 Chinese version for KPW3、KPW4、KV、KO:
https://drive.google.com/file/d/1v17nREeEQHY_er0nxy348u3YS5VkRFuk/view?usp=sharing
-------------------------------------------------------------------------------------------------------------------

---------------------------|Hardware and jailbreak |---------------------------
***hardware requirements of installtion
n31_kte can be installed on the following kindle models:
KPW3,KPW4,KV,KO,KO2,KO3

to install n31_kte on your kindle please jailbreak first, reference link:
https://www.mobileread.com/forums/showthread.php?t=338268

installtion:
0.download n31_kte_xxxxxxx_Vxxx.zip file and unzip it, connect your kindle to pc with USB cable
1.copy RUNME.sh to mnt/us/(the top-level of the visible USB storage, It's the same directory where the documents folder is.)
2.copy the "n31_kte" folder to mnt/us/extensions/
3.open the kindle search bar and type “;log runme”(without the quotation marks), click enter key to run
4..../extensions/n31_kte/txbook/ is n31_kte project folder where you may past your text file that already exists (optional)


----------------------㊀| n31_kte Interface introduction |-----------------------
***Main interface
main UI of n31_kte is divided into three parts:
㊀ | Text Editor |
㊁ | Function Button |
㊂ | Keyboard |


--------------------------㊁|Function button|--------------------------
***0.quick help, new file, quit
quick help: click the [?] button to show/hide quick help.

new file: click the "New" button to create a new text file.
save new file: type a file name(e.g. "test.txt") in text editor, select "test.txt"(without the quotation marks), click save button.

quit n31_kte: click the [Aus┋E] button to quit n31_kte.
*if you can not find [Aus┋E] button, please click the [scro+cal] or [pick-rol] button to hide sub-UI.


***1.open a text file
Click the [Open] button to open the <left slide bar>, then select a text file to open (all text files in .../extensions/n31 kte/txbook/ will be listed in the <left slide bar>).

***2.page up and page down
there are two buttons(with black trigangle symble) that are located in the middle left and middle right of main UI, the left button is for page up, the right button is for page down

***3.location and bookmark
To show/hide the <location bar>, click the [scro+cal] button while nothing is selected in the text editor.
There are three ways to locate the page: a.slide location  b.line number location  c.bookmark

a.location by slide
Slide the grey square button to locate page when the <location bar> is opened (click [scro+cal] to show/hide).

b.location by line number
Enter a line number in the <location bar>, the page will go to that position.

c.bookmarker
Click [bookmark] button to show bookmart list when the <location bar> is opened, click on the certain bookmart to locate the position.
add bookmark: type *** in the front of any line
remove bookmark: delete the ***


***4.accurate text selection
Click the [pick-rpl] button to show/hide <selection bar> while nothing is selected in the text editor.
a.line selection
Click the buttons with white triangle symbols which is on the left side of the <selection bar>.

b.word-by-word selection
Slide grey [square button] to left or right.(this funcation can be used in combination with line selection)

c.select all text
Quadruple click on the grey [square button].


***5.find a word
Select the certain word to be searched in text editor, click the [find & kln] button, all result words will be highlighted, in this state (result words highlighted), click the [fnxt & pic] button, current location will jumped to the next highlighted word
when nothing is selected, click the [find & kln] button to reset search funcation(turn off the highlight words)


***6.word replacement
e.g. to replace word "Apple" to "Orange", type "Apple@*Orange" in text editor and select it(without the quotation marks), then click the [pick-rpl] button,all of "Apple" will be replaced by "Orange", and the replaced words will be highlighted,click the button [find & kln] to turn off highlight.

delete certain words from text editor(=replace the word with empty), e.g. delete all "Apple" from text editor,  type:"Apple@*xxxdelxxx"(without the quotation marks), select it, click the button [pick-rpl], all "Apple" will be deleted.


***7.addtional funcation and settings(<right silde bar>)
To access the <right silde bar>, click the [Hfwd] button in the main UI's middle right corner.
"BgLED__00": turn off background light
"BgLED__09": turn background light to 9

"Ui_lang_CN": change the UI language (between englich an chinese)
"BgLED__21": turn background light to 21 (Flashlight)

"Wifi_switch": turn wifi on/off
"Ssht__i5sec": take a screenshot after you've pressed this button 5 seconds
"Ssvr_switch": turn sceensave on/off (only valid on KO2､KO3)

"EXPLoreR": open external file manager (if "explorer" has been install on default folder)
"TeRMinaL": open external kterm (if "kterm" has been install on default folder)
*how to quit from kterm: use two fingers to touch the screen and then click quit.

"N31>Paint" open the built-in painting board
“Embed-pic” embed a picture into the text (see Advanced Features)
"Cloud>File" download text file from cloud disk, you need configure the Cloud_Lnk.ini file to use this feature.(see Advanced Features)

*Check on [as] checkbox and click "?" button to show Battery, Wifi...state(for PW3, PW4, KO)


***8.save file
If the current file is a new file(that has not been saved), type a file name(e.g. test.txt) in the text editor, select it, click the [save] button.
when current file is a saved file, just click [save] button directly.
Save as a file: type a file name(e.g. test.txt) in the text editor, select it, check on  [as] checkbox, click the [save] button.


---------------------------㊂|keyboard|----------------------------
***1.change the input language
press the "Lang" key on the upper left of the keyboard to change the input language (en, cn ,de)

***2.Send the original inputting characters to | Text Editor |
press the "( )" key on the upper right of the keyboard
* Note, when <input field> is empty (there is no inputting characters), press "( )" key to enter double parentheses.

***3.clean <input field>
press "[°_°]" key on the upper right of the keyboard to clean input field
*Note, when <input field> is empty, press the "[°_°]" key to input '_'｡

***4.to choose Candidate words
when <input field> is not empty, click the [page-up] and [page-dw] buttons to choose Candidate words.
when <input field> is not empty, you can not page-up or page-down text editor, just clean <input field> to restore the functionality.


---------------------------|Advanced Features|----------------------------
***0.calculator
1.check on  [as] checkbox, [scro+cal] button will be changed to [cal+scro]
2.type "(32+56)/7" in to text editor and select it(without the quotation marks), click the [cal+scro] button to get result: 12.57

More calculation sample
Cube values of 4: 4**3
Square roots of 4: 4**0.5

a.Calculate the square of each integer between 1 to 9:
[x*x for x in xrange(1,10)]

b.Calculate each odd square root between 1 to 9 :
[x*x for x in xrange(10) if x%2==1]

c.Calculate each even square root between 1 to 9 :
[x**0.5 for x in xrange(0,10,2)]

d.Calculate the square root of each integer between 1 to 9, the results to keep two decimals :
[round((x**0.5),2) for x in xrange(1,10)]

e.Calculate the integer accumulation value between 1 and 100 :
reduce(lambda x,y: x+y,[x for x in xrange(101)])

f.Calculate sum of 1 to 10 odd square roots and even square roots
map(lambda x,y: x**0.5+y**0.5, [x for x in xrange(1,11) if x%2==0], [y for y in xrange(1,11) if y%2==1])


***1.download text file from cloud disk
a. create a text file in your cloud disk(e.g. google driver)

b. config cloud_lnk.ini first:  .../extensions/n31_kte/txbook/cloud_lnk.ini
   copy download link of the text file, and past it into first line of cloud_lnk.ini, e.g.
   https://ifsbjq.by.files.1drv.com/y4mXgKsqA6pgqhaS0M...

c. click the [Hfwd] button to open <right slide bar>, turn on kindle wifi, and click the "cloud>file",
   the text file will be downloaded in to .../extensions/n31_kte/txbook/, turn off wifi(to prevent amazon OTA your kindle system)


***2.sending Email
a.config cloud_lnk.ini first:  .../extensions/n31_kte/txbook/cloud_lnk.ini
  edit the second line of cloud_lnk.ini:"smtp.live.com::587::mymailbox@hotmail.com::xxxxxxx"(without the quotation marks)
  smtp.live.com: mailbox server(change to yours)
  587: port(change to yours)
  mymailbox@hotmail.com: email address of sender(change to yours)
  xxxxxxx: login password of the email(change to yours)

b.open a text file in n31_kte,type “client_x@gmail.com=regarding_xxx” in the text editor, and select it.(without the quotation marks)
  client_x@gmail.com: mail address of receiver (change to yours)
  regarding_xxx: title of the current mail (change to yours)

c.turn kindle wifi on and check on [as] checkbox.
d.select "client_x@gmail.com=regarding_xxx" and click the [save] button, current text file will be sent to client_x@gmail.com, turn off wifi(to prevent amazon OTA your kindle system)

To use the sending mail function of n31_kte, some mailboxes (such as gmail) must enable the "Allow from External Access" option.
*Note, that the first line of cloud_lnk.ini is the download URL for the cloud file, and the second line is for sending email.


***3.update vocabulary LIB
a.open the file .../extensions/n31_kte/data/english_words_lib.txt (german_words_lib.txt)
b.append your new words at bottom, one line, one word
*Note,Due to the restricted RAM of the kindle, please keep the vocabulary file under 2MB.


***4.seek word
e.g.type: “uni^t” (without the quotation marks) in <input field> with English or German input mode.


***5.empde images in to text file
it is complicated


***6.n31_kte update history
a.add new funcation: bookmark
b.add new funcation: switch UI language
c.add new funcation: embedding image into text
d.add new funcation: shift the spacing review
e.add new funcation: auto open the last edited file
f.add new funcation: system info (for PW3, PW4, KO)
g.optimized: keyboard, paint
h.optimized: pinyin input
i.optimized: UI of n31_kte
j.optimized: text replacement funcation
k.optimized: RAM usage is reduced by 30%, start speed increased by 27%
l.fixed bug: <Text selector >
m.fixed bug: <Page locator >
n.fixed bug: floating window timeout problem
o.update n31_kte help doc
  
https://www.mobileread.com/forums/showthread.php?t=341123
