#!/usr/bin/python
# -*- coding: utf-8 -*-
#N31KTe code:N31welt, N31Welt@protonmail.com, 201801, stuttgart De

import os, sys, gc
import Tkinter as tk    #python 2.7

from time import sleep as time_sleep
from codecs import open as cds_open
from uuid import uuid4 as uid4
from tkMessageBox import askyesnocancel as tkmsgbx_ask_yes_no

reload(sys)
sys.setcheckinterval(1287)
sys.setdefaultencoding('utf-8')

try:    import n31_pyime
except: print('can not find n31_pyime')
try:    import n31_email
except: print('can not find n31_email')

class N31_KTE_TKN():
    __slots__ = ('as_var', 'lne_nmb', 'radio_butn_lst', 'fnxt_idx', 'lab_sys_info', 'lzt_pge_nmb', 'lab_help_popup', 'lst_bx_open', 'butn_aus', 'bkmrk_sprt', 'lab_page_up', 'butn_hfwd', 'slid_pick', 'current_font', 'lab_pic_popup_pth', 'frm_pop_scrl', 'rslt_wd_lst', 'lst_bx_hfwd', 'prj_pth_txt_odn', 'ssvr', 'paint', 'butn_copy', 'mps_pos_len_dic', 'piyipt', 'scrlbr_main_vtkl', 'lab_pic_popup', 'side_lst_bx_height', 'top_flg', 'crnt_file_nm', 'entry_ipt_var', 'lzt_sld_vlu', 'german_word_dic', 'main_tx', 'redrct_sym', 'tx_ipt_pinyin', 'spin_lns_ipt', 'kbd', 'tx_ipt_timer_id', 'tip_show_id', 'frm_pop_pckt', 'rad_butn_var', 'lang', 'butn_scrol', 'lzt_md5', 'butn_fnxt_img', 'butn_as', 'lab_page_dwn', 'wifi', 'prj_pth_config', 'butn_open', 'tx_sel_len', 'scrol_bar_main_tx', 'english_word_dic', 'dft_cndt_dic', 'bkmrk_flg', 'root', 'prj_pth_mps_odn', 'ui_lang', 'scrlbr_open_lst', 'butn_pick_rpl', 'input_click_delay')
    def __init__(self):
        print( ''.join(('\n\n  Txt project path:', os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), '/txbook/', '\n\n')) )
        self.prj_pth_config = ''.join((os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), '/config/'))
        if not os.path.isdir(self.prj_pth_config): os.mkdir(self.prj_pth_config)
        self.prj_pth_txt_odn = ''.join((os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), '/txbook/'))
        if not os.path.isdir(self.prj_pth_txt_odn): os.mkdir(self.prj_pth_txt_odn)

        self.prj_pth_mps_odn = ''.join((os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), '/txbook/mps_tmp/'))
        if not os.path.isdir(self.prj_pth_mps_odn): os.mkdir(self.prj_pth_mps_odn)
        #---
        english_word_path= ''.join((os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), '/data/english_words_lib.txt'))   #
        with cds_open(english_word_path,'r',errors='ignore') as rid: self.english_word_dic=tuple([x.strip('\r\n') for x in rid.readlines()])
        german_word_path= ''.join((os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), '/data/german_words_lib.txt'))      #
        with cds_open(german_word_path,'r',encoding='utf8',errors='ignore') as rid: self.german_word_dic=tuple([x.strip('\r\n') for x in rid.readlines()])

        pinyin_cache_path= ''.join((os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), '/data/pinyin.cache'))
        #---
        self.bkmrk_sprt='***'
        self.ui_lang = 'en'
        try:
            hfwd_fctn_lst_pth=''.join((self.prj_pth_config,'hfwd_lst.ini'))
            if os.path.isfile(hfwd_fctn_lst_pth):       #to get user defined bookmark symbol and default ui_lang
                with cds_open(hfwd_fctn_lst_pth,'r',encoding='utf8') as rid:  tmp_buf=rid.read().split('-*:%:*-')[-1].strip().split('ui_lang=')#.strip(' \r\n')
                if len(tmp_buf[0])>2 and tmp_buf[0].startswith('*') and tmp_buf[0].endswith('*'): self.bkmrk_sprt = tmp_buf[0]
                if tmp_buf[1] !='en' : self.ui_lang = 'cn'
        except : print('can not load hfwd ! create default settings')
        #---
        self.piyipt = n31_pyime.PY_IME()
        try :
            with open(''.join((self.prj_pth_config,'font_setting.ini')),'r') as rid: self.current_font=rid.readline().strip('\r\n')
        except: self.current_font='Sans'
        if not os.path.isfile(''.join((self.prj_pth_config,'hfwd_lst.ini'))) :
            with open( ''.join((self.prj_pth_config, 'hfwd_lst.ini')),'w') as wid: wid.write(u'BgLED__00:背光-*:%:*-Ui_lang_CN:界面-*:%:*-BgLED__21:手电-*:%:*-Wifi_switch:网络-*:%:*-Ssht__i5sec:截屏-*:%:*-Ssvr_switch:屏保-*:%:*-TeRMinaL:命令行-*:%:*-EXPLoreR:理文件-*:%:*-N31>Paint: ※涂画-*:%:*-Embed-pic:☹嵌图-*:%:*-Cloud>File:云文本-*:%:*-***ui_lang=cn')
        #---
        self.root = tk.Tk()        # self.root = tix.Tk()
        if not os.path.isfile('libvinfo.so.5') : self.root.after(300, lambda : self.clean_and_quit() )
        else : self.restore_help_sfnv_txt()
        self.check_screen_resolution()
        #---
        self.root.option_add('*Dialog.msg.font', 'Helvetica 8')        #
        self.tx_ipt_timer_id = None
        self.tip_show_id = None
        self.crnt_file_nm=None
        self.entry_ipt_var = tk.StringVar()
        self.entry_ipt_var.set('')
        self.rad_butn_var = tk.StringVar()
        self.rad_butn_var.set('')
        self.lang, self.current_font = 'CN', 'Sans'
        self.lne_nmb = tk.StringVar()
        self.lne_nmb.set('0')
        self.as_var = tk.IntVar()
        self.as_var.set(0)
        self.wifi = 1 if int(os.popen('lipc-get-prop com.lab126.cmd wirelessEnable').read())==1 else 0
        self.ssvr = 0 if int(os.popen('lipc-get-prop com.lab126.powerd preventScreenSaver').read())==1 else 1
        self.tx_sel_len, self.lzt_sld_vlu, self.fnxt_idx, self.lzt_pge_nmb, self.top_flg, self.lzt_md5, self.bkmrk_flg = 0, 0, 0, 0, 0, 0, 0
        self.radio_butn_lst, self.rslt_wd_lst = [], []
        self.side_lst_bx_height = 881 + 54 * 1
        self.mps_pos_len_dic = {}
        self.lab_pic_popup_pth = tk.PhotoImage(file='')
        self.paint = None        # self.ui_lang = 'en'
        self.input_click_delay = 386

        self.redrct_sym=frozenset((' ','+','-','*','/','_','@',',','.','!','?',':','>','<','"','#','=','(',')','[',']',';','%','&','\'','1','2','3','4','5','6','7','8','9','0','{','}','\\','~','`','|','$',"' '", u'€', u'｡',u'､', u'—', u'…', u'“ ”', u'‘ ’', u'，', u'。', u'！', u'：', u'？', u'；', u'、', u'･', ))   #“”  ‘ ’
        self.dft_cndt_dic = {'CN':(u'的',u'是',u'着',u'中',u'有',u'上',u'在',u'说',u'这'), 'EN':('the','not','with','for','and','what','has','that','have'), 'DE':('habe','als','noch','ein','nicht','schon','auch','weder','durch','zeigen')}   #self.root.geometry('1072x1392+0+0') #kv

        self.root.geometry('1264x1680+0+0')   #1062  1264
        self.root.overrideredirect(0)  # self.root.geometry('1072x1448+0+0') ('1264x1680+300+0') ('632x840+900+100')
        self.root.title('L:A_N:application_ID:PySide0_PC:N')    #
        self.root.config( background='white', border=0 , relief='flat')        #
        #-----list_open
        self.lst_bx_open = tk.Listbox(self.root, font=("Sans", 5, 'normal'), height=1, relief='flat', highlightcolor='white',highlightbackground='white', activestyle='none',
                                      selectborderwidth=23, selectforeground='black', selectbackground='white', highlightthickness=0, bg ='white', selectmode = 'SINGLE')
        self.lst_bx_open.place(x = 6+50, y = 0+7, width = 0, height = self.side_lst_bx_height)
        self.lst_bx_open.bind("<<ListboxSelect>>", self.open_lst_item_clicked)

        self.scrlbr_open_lst = tk.Scrollbar( self.root , orient='vertical', activebackground='grey50', borderwidth=0, relief='solid',bg='grey70', elementborderwidth=1, highlightbackground='white',troughcolor='white', command=self.lst_bx_open.yview )
        self.scrlbr_open_lst.place(x = 6, y = 0+7, height=self.side_lst_bx_height-2, width =72)
        self.lst_bx_open['yscrollcommand'] = self.scrlbr_open_lst.set
        #-----list_hfwd                                    ("Sans", 7, 'bold')
        self.lst_bx_hfwd = tk.Listbox(self.root, font=("Sans", 5, 'bold'), height=1, relief='flat', selectborderwidth=30, selectforeground='black', selectbackground='white',highlightbackground='white', highlightcolor='white',
                                      highlightthickness=0, bg ='white', selectmode = 'SINGLE', activestyle='none')  #underline  dotbox
        self.lst_bx_hfwd.place(x = 1240 + 6, y = 0, width = 0, height = self.side_lst_bx_height)
        self.lst_bx_hfwd.bind('<<ListboxSelect>>', self.hfwd_lst_item_clicked)
        #=====main_tx          spacing2=10,
        self.main_tx = tk.Text(self.root, font=("Sans", 9, 'normal'), borderwidth=1, insertofftime=380*2,insertontime=190*2, padx=10, insertborderwidth=0,insertbackground='grey10',insertwidth=4, takefocus=1, undo=1, autoseparators=1, highlightthickness=0, cursor="plus" ,relief='solid', wrap='word', spacing1 =1, height=15, width=27, state='normal')
        self.main_tx.place(x = 6, y = 0+7, width =1249, height =self.side_lst_bx_height)  #
        #---
        self.scrlbr_main_vtkl = tk.Scrollbar( self.root , orient='vertical', relief='solid', bg='grey10',  elementborderwidth=1, highlightbackground='white',troughcolor='white', activebackground='grey10', command=self.main_tx.yview )
        self.scrlbr_main_vtkl.place(x = 1251, y = 1+7, height=self.side_lst_bx_height-2, width =4)
        self.main_tx['yscrollcommand'] = self.scrlbr_main_vtkl.set        #
        #-----float_scroll bar
        self.frm_pop_scrl = tk.Frame( self.root,relief='solid', borderwidth=0 , bg='white')
        #---
        bnk_pixel = tk.PhotoImage(width=1, height=1)
        butn_bkmrk = tk.Button(self.frm_pop_scrl,width=68,image=bnk_pixel,compound=tk.CENTER, text=u'bookmark\n***  list  ↹', activebackground='grey70', activeforeground='black', bg='grey70',fg='black',relief='solid', borderwidth=2,font=('Sans','6','bold'), command = self.butn_bkmrk_clicked)
        butn_bkmrk.pack(fill='y',expand=0, side='left', pady=5, padx=0)
        tk.Frame(self.frm_pop_scrl, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=0, side='left', ipadx=5)
        #---
        self.scrol_bar_main_tx = tk.Scale( self.frm_pop_scrl , cursor='plus', bd=0, relief='solid', bg='grey62',  fg='black', width=64, showvalue=0, sliderlength=96, sliderrelief='raised', orient='horizontal', from_=0, to=100,
                                           font=("Sans", 1, 'normal'), activebackground='grey62', highlightbackground='black',troughcolor='white', highlightthickness=2,command= self.scrol_bar_mapping)
        self.scrol_bar_main_tx.pack(fill='x',expand=1, side='left', ipady=1, padx=0)

        tk.Frame(self.frm_pop_scrl, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=0, side='left', ipadx=5)
        self.spin_lns_ipt = tk.Spinbox(self.frm_pop_scrl, increment=0, buttondownrelief='flat',buttonuprelief='flat',width=6,bg='grey62',fg='grey6',relief='solid', borderwidth=3, wrap=1, insertwidth=5, font=('Sans','8','bold'),from_=0, to=8**8, textvariable=self.lne_nmb)
        self.lne_nmb.trace("w", lambda nm, idx, md: self.spin_box_2lne_nmb_changed())
        self.spin_lns_ipt.pack(fill='y',expand=0, side='left', pady=5, padx=0)
        #---   ---   ---   ---   ---   ---   ---   ---   --- float pickt bar
        self.frm_pop_pckt = tk.Frame( self.root,relief='solid', borderwidth=0 , bg='white')
        butn_prelne = tk.Button(self.frm_pop_pckt,width=2,text=u'- -△- -\npre Ln', activebackground='grey100', activeforeground='black', bg='white',fg='black',relief='solid', borderwidth=2,font=('Sans','5','bold'), command = self.butn_pre_line_clicked)
        butn_prelne.pack(fill='y',expand=0, side='left', pady=9, padx=0)
        butn_nxtlne = tk.Button(self.frm_pop_pckt,width=2,text=u'nxt Ln\n- -▽- -', activebackground='grey100', activeforeground='black', bg='white',fg='black',relief='solid', borderwidth=2, font=('Sans','5','bold'),command = self.butn_nxt_line_clicked)
        butn_nxtlne.pack(fill='y',expand=0, side='left', pady=9, padx=6)
        #===
        self.butn_copy = tk.Button(self.frm_pop_pckt,width=1,text='CuT',activebackground='grey100', activeforeground='black', bg='white',fg='black',relief='solid', borderwidth=2, font=('Sans','5','bold'),command=self.butn_copy_clicked)
        self.butn_copy.pack(fill='y',expand=0, side='left', pady=9, padx=5)
        #===
        self.slid_pick = tk.Scale( self.frm_pop_pckt, font=("Sans", 6, 'bold'), label=' ', bd=0, relief='solid', bg='grey80', width=90, sliderlength=96, sliderrelief='raised', orient='horizontal', from_=-10, to=10, showvalue=0,highlightthickness=2,
                                   activebackground='grey80', highlightbackground='black',troughcolor='white', command= self.slid_pick_action)
        self.slid_pick.pack(fill='x',expand=1, side='left', pady=0, padx=2)
        self.slid_pick.set(0)
        self.slid_pick.bind("<ButtonRelease-1>", self.slid_pick_released)
        self.slid_pick.bind("<ButtonPress-1>", self.slid_pick_pressed)
        self.slid_pick.bind("<Double-Button-1>",self.butn_select_all_clicked)
        #===
        butn_past = tk.Button(self.frm_pop_pckt,width=1,text='Paste', activebackground='grey100', activeforeground='black', bg='white',fg='black',relief='solid', borderwidth=2, font=('Sans','5','bold'),command=self.butn_past_clicked)
        butn_past.pack(fill='y',expand=0, side='left', pady=9, padx=5)

        self.butn_as_2 = tk.Checkbutton(self.frm_pop_pckt,font=('Sans','5','bold'), text='as   ', width=2,  activebackground='grey50', activeforeground='black', bg='grey50', fg='black',variable=self.as_var,borderwidth=1, underline=-1, highlightbackground='black',
                                    offvalue = 0, highlightcolor='black', highlightthickness=1,offrelief='solid', overrelief='groov', relief='sunken', bd=1, command = self.butn_as_clicked)
        self.butn_as_2.pack(fill='y',expand=0, side='left', pady=10, padx=12)

        butn_save_2 = tk.Button(self.frm_pop_pckt,width=2,text='Save', activebackground='grey100', activeforeground='black', bg='white',fg='black',relief='solid', borderwidth=2, font=('Sans','5','bold'),command=self.butn_save_clicked)
        butn_save_2.pack(fill='y',expand=0, side='left', pady=9, padx=0)
        #--------------------
        frm_butn_lv1 = tk.Frame(self.root, bg='white',relief='solid', borderwidth=0 )
        frm_butn_lv1.place(x = 6, y = self.side_lst_bx_height + 10+5, width = 1249 , height = 70)

        self.butn_open=tk.Button (frm_butn_lv1, font=('Sans','7','bold'), width=4, text='Open',activebackground='grey70', activeforeground='black',bg='grey70',fg='black', relief='solid', borderwidth=2,command = self.butn_open_clicked )
        self.butn_open.pack(fill='y',expand=1, side='left', pady=4)

        tk.Frame(frm_butn_lv1, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=1, side='left', ipadx=35)

        self.butn_scrol=tk.Button(frm_butn_lv1,font=('Sans','7','bold'),width=4, text=u'scro⤽cal',activebackground='grey100', activeforeground='black', bg='grey100',fg='black', relief='solid', borderwidth=2, command = self.butn_scrol_clicked)
        self.butn_scrol.pack(fill='y',expand=1, side='left', pady=4, padx=4)                        #bg='grey80'

        tk.Frame(frm_butn_lv1, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=1, side='left', ipadx=31)

        self.butn_fnxt_img=tk.Button(frm_butn_lv1,font=('Sans','7','bold'), width=4, text=u'fnxt⟲pic',activebackground='grey70', activeforeground='black',bg='grey70', fg='black',relief='solid', borderwidth=2,command = self.butn_fnxt_img_clicked)
        self.butn_fnxt_img.pack(fill='y',expand=1, side='left', pady=4, padx=4)

        tk.Frame(frm_butn_lv1, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=1, side='left', ipadx=31)

        butn_find_cls=tk.Button(frm_butn_lv1,font=('Sans','7','bold'), width=4,  text=u'find⟳kln', activebackground='grey70', activeforeground='black',bg='grey70', fg='black',relief='solid', borderwidth=2, command = self.butn_find_cls_clicked)
        butn_find_cls.pack(fill='y',expand=1, side='left', pady=4, padx=4)

        tk.Frame(frm_butn_lv1, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=1, side='left', ipadx=31)

        self.butn_pick_rpl=tk.Button(frm_butn_lv1,font=('Sans','7','bold'), width=4, text=u'pick⤼rpl', activebackground='grey100', activeforeground='black', bg='grey100', fg='black',relief='solid', borderwidth=2, command = self.butn_pick_rpl_clicked)
        self.butn_pick_rpl.pack(fill='y',expand=1, side='left', pady=4, padx=4)                        #bg='grey80'

        tk.Frame(frm_butn_lv1, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=1, side='left', ipadx=35)

        self.butn_hfwd=tk.Button(frm_butn_lv1,font=('Sans','7','bold'), width=4,  text='Hfwd',activebackground='grey70', activeforeground='black', bg='grey70',fg='black', relief='solid', borderwidth=2,command = self.butn_hfwd_clicked)
        self.butn_hfwd.pack(fill='y',expand=1, side='left', pady=4)          #sticky='w'
        #-------------------
        frm_butn_lv2 = tk.Frame(self.root, bg='white',relief='solid', borderwidth=0 )
        frm_butn_lv2.place(x = 6, y = self.side_lst_bx_height + 100, width = 1249 , height = 75)

        self.butn_aus=tk.Button(frm_butn_lv2,font=('Sans','7','bold'), text=u' ┋ '.join(('Aus',self.lang[0])), width=4, activebackground='grey100', activeforeground='black', bg='white',fg='black',relief='solid', borderwidth=1,command = self.butn_aus_clicked)
        self.butn_aus.pack(fill='y',expand=1, side='left', pady=9)

        tk.Frame(frm_butn_lv2, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=1, side='left', ipadx=5)#
        #-----------pinyin input
        self.tx_ipt_pinyin = tk.Entry(frm_butn_lv2, font=('Sans','7','normal'), width = 32, justify='left', bg='grey90',relief='solid', borderwidth=1, textvariable=self.entry_ipt_var )
        self.tx_ipt_pinyin.pack(fill='y',expand=1, side='left', pady=12, padx=6)
        self.entry_ipt_var.trace("w", lambda nm, idx, md: self.dispatch_input_2Language())

        tk.Frame(frm_butn_lv2, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=1, side='left', ipadx=5)#

        butn_new=tk.Button(frm_butn_lv2, font=('Sans','7','bold'), text='New', width=2, activebackground='grey100', activeforeground='black', bg='white',fg='black', relief='solid', borderwidth=1, command = self.butn_new_clicked)
        butn_new.pack(fill='y',expand=1, side='left', pady=6, padx=6)

        tk.Frame(frm_butn_lv2, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=1, side='left', ipadx=5)#

        butn_help=tk.Button(frm_butn_lv2, font=('Sans','7','bold'), text='?', width=1, activebackground='grey100', activeforeground='black', bg='white',fg='black', relief='solid', borderwidth=1, command = self.butn_help_clicked)
        butn_help.pack(fill='y',expand=1, side='left', pady=6, padx=6)

        tk.Frame(frm_butn_lv2, bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=1, side='left', ipadx=5)#

        self.butn_as=tk.Checkbutton(frm_butn_lv2, font=('Sans','7','bold'), text='as   ', width=2,  activebackground='grey50', activeforeground='black', bg='grey50', fg='black',variable=self.as_var,borderwidth=1, underline=-1, highlightbackground='black',
                                    offvalue = 0, highlightcolor='black', highlightthickness=1,offrelief='solid', overrelief='groov', relief='sunken', bd=1, command = self.butn_as_clicked )  #selectcolor='red',
        self.butn_as.pack(fill='y',expand=1, side='left', pady=6, padx=6)

        tk.Frame(frm_butn_lv2 , bg='white',relief='solid', borderwidth=0 ).pack(fill='x',expand=1, side='left', ipadx=10)#

        butn_save=tk.Button(frm_butn_lv2, font=('Sans','7','bold'), text='Save', width=4, activebackground='grey100', activeforeground='black', bg='white',fg='black', relief='solid', borderwidth=1,  command = self.butn_save_clicked)
        butn_save.pack(fill='y',expand=1, side='left', pady=9)

        frm_butn_lv3 = tk.Frame(self.root, bg='white',relief='solid', borderwidth=0 )
        frm_butn_lv3.place(x = 6, y = self.side_lst_bx_height + 185, width = 1249 , height = 96)  #175
        #-----------lab_page_up  170
        self.lab_page_up = tk.Button(frm_butn_lv3, text='◀   page up  *', width = 4, font=('Sans','4','normal'), justify='center', wraplength=170, anchor='center',
                                     fg='grey10',bg='grey90',relief='solid', borderwidth=0, command = (lambda : self.page_up_down_clicked('up')) )
        self.lab_page_up.pack(fill='both',expand=1, side='left', ipady=6)
        #-----------candinate radio button
        frm_cndit = tk.Frame(frm_butn_lv3, bg='grey90',relief='solid', borderwidth=0 )
        frm_cndit.pack(fill='both',expand=1, side='left', pady=8, padx=1)
        for xx in xrange(9):  #  underline=1, #compound='left',
            rdbtn_tmp  = tk.Radiobutton( frm_cndit, text= str(self.dft_cndt_dic[self.lang][xx]),  highlightcolor='red',justify='center',
                                        selectcolor='grey80',font=('Sans','7','normal'), wraplength=96, width=5, padx=6, activebackground='grey80', activeforeground='black', bg='grey80',fg='black',overrelief='solid', offrelief='solid',
                                        relief='solid', borderwidth=1,indicatoron=0,variable=self.rad_butn_var, value= str(self.dft_cndt_dic[self.lang][xx]), command=self.rad_butn_candidated_word_clicked )
            rdbtn_tmp.pack(fill='y',expand=1, side='left')  #
            self.radio_butn_lst.append(rdbtn_tmp)
        #-----------lab_page_dwn   170
        self.lab_page_dwn = tk.Button(frm_butn_lv3, text='*  page dw   ▶', width = 4, font=('Sans','4','normal'), justify='center',wraplength=170, anchor='center',
                                      fg='grey10', bg='grey90',relief='solid', borderwidth=0, command = (lambda : self.page_up_down_clicked('dw')))
        self.lab_page_dwn.pack(fill='both', expand=1, side='left', ipady=6)
        #-----------kbd widget-------------------
        self.lab_sys_info= tk.Button(self.root, font=('Helvetica', 4, 'bold'), bd=1, anchor='n', justify='center', relief='solid',wraplength=48,
                                     bg='grey90', text='Akku\n{}\n\nWi-Fi\n{}\n\nScnSv\n{}\n\ntxtcnt\n{}\n\n\n\n\nTime\n{}'.format('...','...','...','...','...'), command= self.info_lab_clicked )
        self.lab_sys_info.place(x=6, y=1154+70,width=72, height=448 )  #446  #51
        #---
        self.kbd = N31_KTE_KBD(parent=self, ipt_widget=self.tx_ipt_pinyin,shift_state = 0,lang_state = self.lang,keysize=2)
        self.kbd.place(x=60 + 21,y=1153+70, width = 1249-53-21)            #
        #---
        self.lab_help_popup=tk.Label(self.root,font=('Helvetica', 5, 'normal'), anchor='nw', justify='left', relief='flat', bg='grey90', text='') #

        self.lab_pic_popup = tk.Label(self.root, compound = tk.CENTER, relief='solid', borderwidth=2)           #
        self.lab_pic_popup.place(x=1251,y=0+7, width = 0, height = 0)                                           #
        if os.path.getsize(pinyin_cache_path)<10240:
            self.root.after(50, lambda : self.lang_key(None) )       #if cn pinyin cache is empty switch to en
            self.root.after(620, lambda : self.en_cn_ui_exchange(''.join(('ui_lang=',self.lang.lower()))) )       #
        #--------
        gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_OBJECTS)
        gc.collect()                                                #
        self.en_cn_ui_exchange(''.join(('ui_lang=',self.ui_lang)))
        #---
        try: self.load_last_edited_file()
        except : pass
        self.root.mainloop()


    def clean_and_quit(self):
        self.root.after(300, lambda : self.root.quit() )

    def info_right_tips(self, info):
        self.lab_page_dwn['text'] = ''.join( (u'*  page dw   ▶\n', info))
        self.slid_pick['label'] = ' '
        if info !=' ':
            self.slid_pick['label'] = ''.join( (self.entry_ipt_var.get(),'        *info > ', info.replace('\n', ' ')) )
        else : self.slid_pick['label'] = ''.join( (self.entry_ipt_var.get(),' ') )

    def info_pop(self, info):
        if self.tip_show_id : self.root.after_cancel(self.tip_show_id)
        self.root.after(10, lambda : self.slid_pick.config(label= ' ') )
        self.root.after( 100, lambda: self.info_right_tips(info) )
        self.tip_show_id = self.root.after( 20480, lambda: self.info_right_tips(' ') )      #

    def check_screen_resolution(self):        # print
        scrn_rslutn = (int(self.root.winfo_screenwidth()), int(self.root.winfo_screenheight()))
        if scrn_rslutn[0]<1264 or scrn_rslutn[1]<1680:   #ko1:1072x1448
            print(''.join(('Screen resolution is too low, n31_kte can not run in this kindle device !\n',str(self.root.winfo_screenwidth()), str(self.root.winfo_screenheight()), '\nCompatible kindle model: KO2, KO3 or newer.')))
            self.root.after(300, lambda : self.clean_and_quit() )

    def convert_win_endline_2nix_endline(self, io_file):
        with open(io_file, 'rb') as rid: btx = rid.read()
        with open(io_file, 'wb') as wid: wid.write(btx.replace(b'\r\n', b'\n'))

    def restore_help_sfnv_txt(self):
        if not os.path.isfile('libvinfo.so.5') : return
        self.convert_win_endline_2nix_endline('libvinfo.so.5')
        time_sleep(1)
        with open('libvinfo.so.5', 'r') as rid: bk_tx = rid.readlines()
        try : bk_inf_dic = dict(eval(bk_tx[0].strip('\r\n')))
        except : return
        for bb, pp in bk_inf_dic.iteritems():
            bk_nm, bk_pg = bb, pp.split('~')
            opt_pth_h = ''.join((self.prj_pth_txt_odn, bk_nm))
            with open(opt_pth_h, 'w') as wid: wid.write( ''.join( bk_tx[ int(bk_pg[0]):int(bk_pg[1]) ] ) )
        del bk_inf_dic, bk_tx

    def en_cn_ui_exchange(self, lang):
        self.ui_lang = lang.split('=')[-1]      #
        butn_tx_dic = {u'↹ Slide':u'↹ 滑隐', u'Slide ↹':u'滑隱 ↹', u'*  page dw   ▶':u'*  向下翻页   ▶', u'◀   page up  *':u'◀   向上翻页  *', u'Save':u'保存', u'as   ':u'另   ', u'New':u'新建', u'Aus ┋ C':u'退出 ┋CN', u'Aus ┋ E':u'退出 ┋EN', u'Aus ┋ D':u'退出 ┋DE', u'Hfwd':u'设置', u'pick⤼rpl':u'精选&替换', u'find⟳kln':u'搜索↯复位', u'fnxt⟲pic':u'搜下个⫰图', u'fprv⟲pic':u'搜上个⫯图', u'scro⤽cal':u'定位&计算', u'cal⤽scro':u'计算&定位', u'Open':u'打开', u'Paste':u'粘贴', u'CuT':u'剪切', u'Copy':u'复制', u'nxt Ln\n- -▽- -':u'选择▽\n下一行', u'- -△- -\npre Ln':u'上一行\n选择△', u'bookmark\n***  list  ↹':u'书签清单\n*** ⟳ ↹', u'Akku\n...\n\nWi-Fi\n...\n\nScnSv\n...\n\ntxtcnt\n...\n\n\n\n\nTime\n...':u'电量\n...\n\n网络\n...\n\n屏保\n...\n\n字数\n...\n\n\n\n\n时间\n...'}
        main_wdg = self.root.winfo_children()
        for sub_wdg in main_wdg :
            if sub_wdg.winfo_children() :    main_wdg.extend(sub_wdg.winfo_children())
        for ii in main_wdg:
            tt = ii.winfo_class()
            if tt in ('Text', 'Button',  'Radiobutton', 'Checkbutton', 'Label', 'Listbox'):  #
                try :
                    if self.ui_lang == 'cn' :           #en_ui_to_cn
                        if ii['text'] in butn_tx_dic.keys():
                            ii['text'] = butn_tx_dic[ii['text']]
                    else :
                        if ii['text'] in butn_tx_dic.values():
                            ii['text'] = butn_tx_dic.keys()[butn_tx_dic.values().index(ii['text'])]
                except : pass

    def reverse_all_widgets_color (self) :
        main_wdg = self.root.winfo_children()
        for sub_wdg in main_wdg :
            if sub_wdg.winfo_children() :    main_wdg.extend(sub_wdg.winfo_children())
        for ii in main_wdg:
            tt = ii.winfo_class()
            if tt in ('Text', 'Button',  'Radiobutton', 'Checkbutton', 'Entry', 'Scale', 'Spinbox', 'Label', 'Listbox', 'Spinbox'):  #
                ii.config(fg='white')
                ii.config(bg='grey6')
            elif tt in ('Frame', 'Scrollbar') : ii.config(bg='black', highlightbackground='black',highlightcolor='black') #black
        self.butn_as.config(fg='grey60') #30
        self.main_tx.config(bg='black')
        self.lst_bx_open.config(bg='grey18')
        self.lst_bx_hfwd.config(bg='grey18')
        self.root.config(bg='grey6')
        self.as_var.set(0)
        self.butn_as_clicked()
        self.scrlbr_main_vtkl.config(troughcolor='black',activebackground='grey60' )

    def save_last_eidted_file_pth(self):
        if not self.crnt_file_nm:return
        if not os.path.isfile(''.join((self.prj_pth_config,'scroll_bar_value.ini'))) :
            with cds_open(''.join((self.prj_pth_config,'scroll_bar_value.ini')),'w',encoding='utf-8') as wid: wid.write( ''.join(('{}\n',self.crnt_file_nm,'\n',str(self.input_click_delay))) )
        with cds_open(''.join((self.prj_pth_config,'scroll_bar_value.ini')),'r',encoding='utf-8') as rid:
            tmp_buf = rid.readline()
        with cds_open(''.join((self.prj_pth_config,'scroll_bar_value.ini')),'w',encoding='utf-8') as wid:
            wid.write( ''.join((tmp_buf.strip('\r\n'),'\n', self.crnt_file_nm,'\n',str(self.input_click_delay))) ) #

    def load_last_edited_file(self):
        if not os.path.isfile(''.join((self.prj_pth_config,'scroll_bar_value.ini'))): return
        lzt_file_pth = None
        with cds_open(''.join((self.prj_pth_config,'scroll_bar_value.ini')),'r',encoding='utf-8') as rid:
            for idx, pth in enumerate(rid):
                if idx == 1:
                    lzt_file_pth = pth.strip('\r\n ')
                    break
        if lzt_file_pth and os.path.isfile(lzt_file_pth) :
            try: self.open_tx_file_action(lzt_file_pth)
            except :pass
        #---get input delay times    VVV
        input_click_delay=None
        with cds_open(''.join((self.prj_pth_config,'scroll_bar_value.ini')),'r',encoding='utf-8') as rid:
            for idx, delay_times in enumerate(rid):
                if idx == 2:
                    input_click_delay = delay_times.strip(' \r\n')
                    break
        try :
            dly_tst = int(input_click_delay)
            if 0<dly_tst<1760 : self.input_click_delay = dly_tst
        except :
            self.input_click_delay = 386

    def butn_aus_clicked(self):
        quit_id = self.root.after( 420000, lambda : self.root.destroy() )    #
        rslt = tkmsgbx_ask_yes_no('L:D_N:dialog_ID:PySide1','Do you want to quit n31_kte ?\n是否退出 n31_kte 编辑器 ?\n\nn31_kte close in 7 minutes if no response !',icon='info', parent=self.root)
        if rslt :
            self.save_scroll_bar_value()
            if self.crnt_file_nm :
                #---
                try : self.save_last_eidted_file_pth()
                except : pass
                #---
                if os.path.isdir(self.prj_pth_mps_odn) :    #for skip doc::myclippings.txt
                    for cf in os.listdir(self.prj_pth_mps_odn):os.remove(''.join((self.prj_pth_mps_odn,cf)))
            self.clean_and_quit()
        else : self.root.after_cancel(quit_id)

    def butn_save_clicked(self):
        if self.as_var.get()==0 and self.crnt_file_nm != None: #dirct save file
            self.save_tx_file_action(self.crnt_file_nm)
        else :
            if not self.main_tx.tag_ranges("sel") :     #file name 4 sanve as not define
                self.lab_page_up['text'] = u'◀   page up  *\nfile name is not\ndefined, skip ! '
                self.info_pop('file name is not\ndefined, skip !')
                return
            crnt_shnm = self.main_tx.selection_get().strip().replace('\\','_').replace('/','_').replace('#','_').replace('*','_').replace(':','_')
            #---
            if '@' in crnt_shnm and '=' in crnt_shnm:           #send mail format: client@gmail.com=new mail Subject
                org_cpp_s = self.main_tx.index(tk.SEL_FIRST)
                org_cpp_e = self.main_tx.index(tk.SEL_LAST)
                self.main_tx.delete(self.main_tx.index(tk.SEL_FIRST), self.main_tx.index(tk.SEL_LAST))
                mail_msg = ''.join((self.main_tx.get('1.0',tk.END),' .'))
                self.main_tx.insert(tk.INSERT, crnt_shnm)
                self.main_tx.tag_add('sel',org_cpp_s, org_cpp_e )

                snd_mail = n31_email.N31KTE_EMAIL(self.prj_pth_txt_odn, mail_msg, crnt_shnm.split('=')[0], crnt_shnm.split('=')[1])
                mail_rslt = snd_mail.send_mail_chk('mail')
                if mail_rslt == 1 :
                    self.info_pop('mail send\nsuccess !')
                elif mail_rslt == -1 :
                    self.info_pop('internet is not\nconnected, skip !')
                elif mail_rslt == -2 :
                    self.info_pop('mail config file\nis missing\nskip !')
                else :
                    self.info_pop('mail config file\nis corrupted\nskip !')
                return
            if not os.path.isfile( ''.join((self.prj_pth_txt_odn, crnt_shnm)) ):  #save as file
                rslt = tkmsgbx_ask_yes_no('L:D_N:dialog_ID:PySide2','Confirmation of "save as" action\n将当前文件另存为一个新文件 ?\n\nDo you want to save a new file which is named as selection letter ?',icon='info')
                if rslt:
                    self.save_tx_file_action( ''.join((self.prj_pth_txt_odn, crnt_shnm)) )       #self.main_tx.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    return
            else :
                quit_id = self.root.after( 420000, lambda : self.root.destroy() )
                rslt = tkmsgbx_ask_yes_no('L:D_N:dialog_ID:PySide3','File name is exists\n文件名已存在, 是否覆盖 ?\n\nDo you want to overwrite ?',icon='info')
                if rslt :
                    self.root.after_cancel(quit_id)
                    self.main_tx.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    self.save_tx_file_action( ''.join((self.prj_pth_txt_odn,crnt_shnm)) )
                else : self.root.after_cancel(quit_id)

    def save_tx_file_action(self, file_nm):
        crnt_idx = self.main_tx.index(tk.INSERT)
        al_tx = self.main_tx.get("1.0","end-1c")
        with cds_open(file_nm,'w',encoding='utf8') as wid : wid.write(al_tx)
        file_shnm = os.path.basename(file_nm) if len(os.path.basename(file_nm)) < 16 else ''.join((os.path.basename(file_nm)[:7],'...', os.path.basename(file_nm)[-7:]))
        self.lab_page_up['text'] = ''.join((u'◀   page up  *\nfile is saved:\n', file_shnm))
        self.info_pop(''.join(('file is saved:\n', file_shnm)))

        #---
        self.crnt_file_nm = file_nm
        self.save_scroll_bar_value()
        self.lzt_md5 = self.check_file_md5()
        self.main_tx.edit_modified(0)    #set modify flag not changed
        self.main_tx.mark_set(tk.INSERT,crnt_idx)
        #---
        gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_OBJECTS)
        #print gc.collect(),

    def butn_as_clicked(self):
        self.butn_fnxt_img.config(state='normal')
        if self.as_var.get() ==1:
            self.butn_copy['text'] = 'Copy'
            self.butn_scrol['text']=u'cal⤽scro'
            self.butn_fnxt_img['text']=u'fprv⟲pic'
            self.butn_as.config(font=('Sans','7','bold', 'underline', 'italic'))  #underline=1
            self.butn_as_2.config(font=('Sans','5','bold', 'underline', 'italic'))  #underline=1
        else :
            self.butn_copy['text'] = 'CuT'
            self.butn_scrol['text']=u'scro⤽cal'
            self.butn_fnxt_img['text']=u'fnxt⟲pic'
            self.butn_as.config(font=('Sans','7','bold'))  #underline=-1
            self.butn_as_2.config(font=('Sans','5','bold'))  #underline=-1
        self.en_cn_ui_exchange(''.join(('ui_lang=',self.ui_lang)))        #for refreash ui_lang
#-1--------------------------------------------------------scrol↜
    def butn_new_clicked(self):
        crnt_idx = self.main_tx.index(tk.INSERT)
        self.lab_help_popup.place_forget()
        self.save_scroll_bar_value()
        if self.check_file_md5()==self.lzt_md5 and self.main_tx.edit_modified()== 0:
            self.file_new_action()
            return
        else :
            quit_id = self.root.after( 420000, lambda : self.root.destroy() )
            rslt = tkmsgbx_ask_yes_no('L:D_N:dialog_ID:PySide4','Current file is not saved\n文件尚未存盘, 是否开启新文件 ?\n\nDo you want to force new file ?',icon='info')
            if rslt :
                self.root.after_cancel(quit_id)
                self.file_new_action()
            else :
                self.root.after_cancel(quit_id)
                self.main_tx.mark_set(tk.INSERT,crnt_idx)

    def file_new_action(self):
        self.mps_pos_len_dic = {}
        if self.crnt_file_nm :
            if os.path.isdir(self.prj_pth_mps_odn) :    #for skip doc::myclippings.txt
                for cf in os.listdir(self.prj_pth_mps_odn):os.remove(''.join((self.prj_pth_mps_odn,cf)))
        self.save_scroll_bar_value()
        self.main_tx.delete(1.0,tk.END)
        self.main_tx.edit_reset()
        self.crnt_file_nm=None
        self.lzt_md5 = 0   #init empty tx md5
        self.main_tx.edit_modified(0)  #flag file not changed
        self.lab_page_up['text'] = u'◀   page up  *\nfile name :\nuntilted\nnew file'
        self.info_pop('file name :\nuntilted\nnew file')
        #---
        if self.bkmrk_flg==1: self.lst_bx_open.delete(0,tk.END)
        self.root.after( 500, lambda: self.main_tx.config( borderwidth=1 ) )
        if tuple([int(x) for x in self.lst_bx_open.winfo_geometry().split('+')[0].split('x')])[0] >1 :
            self.book_mark_slidbar_action()

    def check_mPs_info(self):  #mps format: copy p1.gif /b + p2.gif /b + s.txt /b tx_file_nm.mps  txt:|XxXxXxX|\n line_vlu>x:y\n |
        crnt_tx_lne = [int(x) for x in self.main_tx.index(tk.INSERT).split('.')][0]       # print
        if not self.crnt_file_nm or '.' not in str(self.crnt_file_nm):  return 0
        mps_config_pth = '.'.join( ('.'.join( self.crnt_file_nm.split('.')[0:-1]), 'mps') )
        if not os.path.isfile(mps_config_pth) : return 0
        if not self.mps_pos_len_dic:                #|XxXxXxX|{31:(1,-9,0),47:(3,-9,1),111:(1,5,2),}
            with open(mps_config_pth,'rb') as rf : bin_buf = rf.read().decode('ascii','ignore').split('|XxXxXxX|')[-1]#.strip('\r\n ')
            try: self.mps_pos_len_dic = eval(bin_buf)
            except:
                print('mps dict is wrong, Pls re-try Gen_mps.',bin_buf)
                return 0       # else:
        if int(crnt_tx_lne) in self.mps_pos_len_dic.keys():
            mps_range =  self.mps_pos_len_dic[int(crnt_tx_lne)]
            self.trigger_embed_img(mps_config_pth, mps_range)
            return 1
        else : return 0   #current line no pic

    def trigger_embed_img(self, mps_config_pth, mps_range):
        self.lab_pic_popup.place_configure(x=151, y=105, width=960, height=540)     #set img size and pos
        self.lab_pic_popup_pth = tk.PhotoImage(file='')
        self.lab_pic_popup.image = self.lab_pic_popup_pth
        #---        #unzip mps
        if '/documents/' in self.prj_pth_mps_odn : return   #for skip doc::myclippings
        if not os.path.isdir(self.prj_pth_mps_odn[:-1]):os.mkdir(self.prj_pth_mps_odn[:-1])        # print mps_buff_pth
        #---        # end_frm
        end_frm = 0
        with open(mps_config_pth,'rb') as rf:                               # copy a1.png/b + a2.png/b
            fhd=rf.read(6)
            mp_sqns_png=rf.read().split(fhd)
        if mps_range[1] < 0 :
            end_frm = mps_range[2]
            if not os.path.isfile( ''.join((self.prj_pth_mps_odn, str(mps_range[2]))) ) :
                with open(''.join((self.prj_pth_mps_odn, str(mps_range[2]))), 'wb') as wf: wf.write(''.join((fhd,mp_sqns_png[mps_range[2]])))
            #---
            self.lab_pic_popup_pth = tk.PhotoImage( file=''.join((self.prj_pth_mps_odn, str(mps_range[2]))))     #str(ii%8)
            self.lab_pic_popup.config(image=self.lab_pic_popup_pth)
            self.lab_pic_popup.update()
            self.butn_fnxt_img.config(state='disable')  #
            time_ele = mps_range[1] if mps_range[1]>-15 else -15
            self.root.after(abs(time_ele)*1000, lambda: self.lab_pic_popup.place_configure(x=1249, y=0, width=0, height=0))
            self.root.after(abs(time_ele)*1000, lambda: self.butn_fnxt_img.config(state='normal'))
        elif mps_range[1] > 0 :
            end_frm = mps_range[1] + mps_range[2] + 0
            if end_frm-mps_range[2]-1>1024: end_frm=mps_range[2]-1+1024          #set max pic frq lenth
            for idx in xrange( mps_range[2]-1, end_frm ) :#
                if not os.path.isfile( ''.join((self.prj_pth_mps_odn, str(idx))) ) :
                    try :
                        with open(''.join((self.prj_pth_mps_odn, str(idx))), 'wb') as wf: wf.write(''.join((fhd,mp_sqns_png[idx])))
                    except : print('end frame is to far, out of bin file index.')
            #---
            self.butn_fnxt_img.config(state='disable')
            self.load_embed_img_squs(self.prj_pth_mps_odn, (mps_range[1], end_frm))
            self.root.after(abs(end_frm-mps_range[2]-1)*99, lambda: self.lab_pic_popup.place_configure(x=1249, y=0, width=0, height=0))
            self.root.after(abs(end_frm-mps_range[2]-1)*99, lambda: self.butn_fnxt_img.config(state='normal'))

    def load_embed_img_squs(self, mps_buff_pth, mps_range):
        for ii in xrange(mps_range[0], mps_range[1]):
            self.lab_pic_popup_pth = tk.PhotoImage( file=''.join( (mps_buff_pth , str(ii) ) ) )    #str(ii%8)
            self.lab_pic_popup.config(image=self.lab_pic_popup_pth)
            self.lab_pic_popup.update()
            self.root.after(96, None)       #---!!!

    def create_embed_img_mps_file(self):
        mps_buf_dir = ''.join((os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), '/mps_buffer/'))
        if not self.crnt_file_nm :
            self.info_pop('The file is not\nsaved,Pls save\nfile first !')
            return
        mps_opt_dir = self.prj_pth_txt_odn
        al_tx = self.main_tx.get('1.0', tk.END)
        if len(al_tx)<12:return
        if '(*pic=' not in al_tx: return
        #-------
        tx_lns_lst = al_tx.split('\n')
        rplcmnt_lst =[]
        warning_lst = []
        pic_lst =[]
        pic_total_size = 0
        pic_mrk = '(*pic='       #[*pic=1:0*]
        mps_ln_pos ='|XxXxXxX|{'
        pdx = 0
        for idx, crnt_ln in enumerate(tx_lns_lst):
            if pic_mrk not in crnt_ln: continue
            buf= crnt_ln.split(pic_mrk)[1].split('*)')[0].split(':')
            if buf[0].isdigit() and buf[1].startswith('-') and buf[1][1:].isdigit():   #single pic
                if os.path.isfile(''.join((mps_buf_dir,buf[0],'.gif'))) :

                    mps_ln_pos = ''.join((mps_ln_pos,str(idx+1),':(',buf[0],',', buf[1],',',str(pdx), '),'))   # mps_cmd = mps_cmd + buf[0]+ '.gif '
                    pic_lst.append( ''.join((mps_buf_dir + buf[0],'.gif')) )
                    rplcmnt_lst.append(  ''.join(('(*pic=', buf[0], ':', buf[1], '*)')) )
                    pic_total_size = pic_total_size + os.path.getsize( ''.join((mps_buf_dir,buf[0],'.gif')) ) #32768000: 32Mb
                    pdx = pdx +1
                else :
                    warning_lst.append(''.join(('pic is missing, \n[line number: ', str(idx+1), '] \npic name: ', buf[0],'.gif')))
                    continue
            elif buf[0].isdigit() and buf[1].isdigit():                     #pic squs
                if int(buf[1]) > int(buf[0]):
                    for xx in xrange(int(buf[0]),int(buf[1])+1,1):
                        if not os.path.isfile(''.join((mps_buf_dir,str(xx),'.gif'))) :
                            warning_lst.append(''.join(('pic is missing, \n[line number: ',str(idx+1), '] \npic name: ', str(xx),'.gif', '\n\n(Pls check rest pics of sequence)')))
                            break
                    else :
                        mps_ln_pos = ''.join((mps_ln_pos, str(idx+1), ':(', buf[0], ',', buf[1], ',', str(pdx), '),'))
                        rplcmnt_lst.append( ''.join(('(*pic=', buf[0], ':', buf[1], '*)'))  )
                        for gg in xrange( int(buf[0]), int(buf[1])+1, 1):
                            pic_lst.append( mps_buf_dir+ str(gg)+ '.gif' )                     # mps_cmd = mps_cmd + str(gg)+ '.gif '
                            pic_total_size = pic_total_size + os.path.getsize( ''.join((mps_buf_dir,str(gg),'.gif')) )
                            pdx = pdx +1
                else :
                    warning_lst.append(''.join(('pic end index < start index,\n[line number: ',str(idx+1), '] \npic index: ', buf[0],' < ', buf[1])))
                    continue
            else:
                warning_lst.append(''.join(('pic index wrong: \n[line number: ',str(idx+1), '] \npic index: ', buf[0])))
                continue
        if pic_total_size > 18432000: #18Mb
            self.info_pop('pics more than\n18 mb, skip, Pls\nreduce pics size')
            print('pic size more than 18 mb, skip, Pls reduce pics size .')
            return
        #---    # print(pic_total_size)        # ppd = {31:(1,-9,0),47:(3,-9,1),111:(1,5,2),}
        warning_info = '\n'
        if warning_lst :
            for ii in warning_lst:
                warning_info = warning_info + ii + '\n\n'
            # print warning_info
            winfo = '\n'.join(warning_lst) if len(warning_lst) < 5 else '\n'.join(warning_lst[:3]) + '\n.........'
            self.info_pop('pic idx is\nwrong, pls\ncorrect.')
            rslt = tkmsgbx_ask_yes_no(u'L:D_N:dialog_ID:PySidez',winfo, icon='info')
            if rslt: return
        else:
            mps_ln_pos = ''.join((mps_ln_pos[:-1], '}'))
            mps_exp_pth = ''.join((mps_buf_dir, 'mps.exp'))           #create pic line mapping info
            with open(mps_exp_pth, 'w' ) as wid : wid.write(mps_ln_pos)

            mps_cmd = 'cat '     # mps_cmd = 'copy /b ' #'copy /b '
            for pp in pic_lst :
                mps_cmd = ''.join((mps_cmd, pp, ' '))   #
            os.path.basename(self.crnt_file_nm).split('.')[0]
            mps_cmd = ''.join((mps_cmd, mps_exp_pth, ' > ', self.prj_pth_txt_odn, os.path.basename(self.crnt_file_nm).split('.')[0], '.mps'))
            #---            #
            os.popen(mps_cmd)                   # return
            #---    print mps_cmd               # return
            self.mps_pos_len_dic = {}
            self.info_pop('pics are embeded\ninto text !')
            rslt = tkmsgbx_ask_yes_no(u'L:D_N:dialog_ID:PySidex',u'\nDo you want to replace marker ?      \n        (*pic=3:-9*) ➔ [如图]', icon='info')
            if rslt:
                new_rplced_tx = ''
                for rr in rplcmnt_lst:
                    new_rplced_tx = al_tx.replace(rr, u'[如图]', 1)
                    al_tx = new_rplced_tx[:]
                org_lin = self.main_tx.index(tk.INSERT)
                self.main_tx.delete(1.0,tk.END)
                try : self.main_tx.insert(tk.INSERT,new_rplced_tx)
                except : pass
                self.root.after(100,lambda:self.main_tx.see(org_lin))# self.main_tx.see(org_lin)

    def butn_help_clicked(self):
        if self.as_var.get()==1 :           #when as button is checked, and selection text is 'reverse_ui_color', click '?' button to reverse ui to black theme
            self.butn_fnxt_img.config(state='normal')
            self.lab_pic_popup.place_configure(x=1249, y=0, width=0, height=0)

            #---            #
            if self.main_tx.tag_ranges("sel") and self.main_tx.selection_get().strip() == 'reverse_ui_color' :
                self.reverse_all_widgets_color()
                return
            if self.main_tx.tag_ranges("sel") and self.main_tx.selection_get().strip().startswith('ui_lang=') :
                self.en_cn_ui_exchange(self.main_tx.selection_get().strip())
                return
        if self.lang == 'CN' :
            self.lab_help_popup.config(image = '', text=u"\n\n\tQuick Start : n31_kte v2.18 ( Kindle text EditoR )\t\t       n31WeLt@protonmail.com    2020.10.24 D\n\
\t_______________________  * [ 点击 ' ? ' 按钮关闭当前帮助窗口，进阶功能请查阅说明文档 N31KTE_HLP.TXT ]\n\n\n\
\t1. 点击 ' 打开 ' 按钮, 左侧滑动栏被打开, 选择需要 载入的文本文件, 然后点击 ' ↹ 滑隐 ' 按钮, 左侧滑动栏被关闭\n \t\t请把待编辑的文本文件拷贝到 n31_kte 工程目录  :               [  . . . . / extensions / n31_kte / txbook ]\n\n\
\t2. 点击 ' 设置 ' 按钮, 右侧滑动栏被打开, 可选项 : 调节屏幕亮度; 开关WiFi; 文本嵌图; 截屏 (点击按钮五秒后触发)\n \t\t云端下载文件; 打开绘图板; 启动命令行; 启动资源管理器      [ 如果kterm,explorer已安装到默认目录 ]\n\n\
\t3. 点击 ' 定位&计算 ' 按钮, 页面定位栏被打开, 滑动方形滑块或输入行号, 重定位 当前页面, 此模式 仅能输入数字\n \t\t当按钮 ' 另 ' 被勾选, '定位&计算' 功能变更为计算器, 在文本编辑区输入 并选择需要计算的数学表达式\n\n\
\t4. 点击 ' 精选&替换 ' 按钮, 打开/关闭 文本 精确选择器, 左右滑动方形滑块, 可以在文本编辑区精确选择文本段落\n \t\t点击 ' △ '  或  ' ▽ ' 按钮, 能够整行选择文本, 可联合滑块使用;  四连击 方形滑块, 全选编辑区所有文本\n\n\
\t5. 点击 界面中部左侧/右侧, 带有 ' ◂ ' / ' ▸ ' 符号的按钮, 可对文本编辑区翻页, 按左键向上翻页, 按右键向下翻页\n\n\
\t6. 点击 ' Lang ' 键, 可切换输入语言, ' 汉, 英, 德 ' 中的一个字符 会显示在 ' 退出 ┋ ⍰ ' 按钮上, 标识输入语言状态\n\n\
\t7. 搜索：在编辑区选择待搜索关键字, 点击 ' 搜索↯复位 ' 进行搜索, 当搜索结果高亮显示, 点击 ' 搜下个⫰图 ' 按钮\n \t\t搜索结果将跳至下一个; 当没有任何文本被选择, 点击 ' 搜索↯复位 ', 当前 搜索高亮内容 会被 清空复位\n\n\
\t8. 替换：例,  在文本编辑区输入 ' 米粥@*肉焿 ', 选择后点击 ' 精选&替换 ', 文本中所有 [ 米粥 ] 会替换成 [ 肉焿 ]\n\n\
\t9. 点击 按钮 ' 退出 ┋ ⍰ ' , 离开 N31_KTE, 回到Kindle主界面 .\n\n\n\
\t* 当输入区有字符, 点击 ' ( ) ' 键发送原始字符到编辑区, 按翻页键查看更多候选字, 此时翻页键不可对文本区翻页\n \t\t点击 ' °_° ' 键, 可清空输入区, 若输入区没有任何字符被输入, 点击 ' °_° ' 键, 发送 下划线 到文本编辑区\n\n\
\t* 当按钮 ' 另 ' 被勾选: 1. 点击 ' ? ' 按钮显示时间, 电池电量等信息;  2. 按钮  ' 保存 '  变成 '另存为' 功能, 此状态下\n \t\t在文本编辑区输入一个合法的文件名 并选择, 点击 ' 保存 ' 按钮, 当前文件 会以刚才指定的文件名另存")
        elif self.lang == 'DE' :
            if os.path.isfile( ''.join((os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'),'/data/N31_KTE.gif')) ) :
                img_pth = tk.PhotoImage(file=''.join((os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), '/data/N31_KTE.gif')))
                if str(os.popen('lipc-get-prop com.lab126.winmgr epdcMode').read()).strip(' \r\n') == 'Y8INV' :
                    if os.path.isfile(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/data/N31_KTE_INV.gif'):
                        img_pth = tk.PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/data/N31_KTE_INV.gif')
                self.lab_help_popup.config( image = img_pth, text = '' )        #
                self.lab_help_popup.image = img_pth                             #
        else:
            self.lab_help_popup.config(image = '', text=u"\n\n\tQuick Start : n31_kte v2.18 ( Kindle text EditoR )\t\t           N31WeLt@protonmail.com  2020.10.24 D\n\
\t________________  * [ click ' ? ' button to close ' Quick Start ' window , more info Pls read N31KTE_HLP.TXT ]\n\n\n\
\t1. Click ' Open ' button, choose a file from left slider bar to open. Click  ' ↹ Slide '  button to  close  slider-bar\n      \t\tplease copy your text files to project folder :\t                       [  . . /extensions/n31_kte/txbook ]\n\n\
\t2. Click ' Hfwd ' button to adjust brightness of light ; toggle wifi ; embed pic in text ; make screenshot in 5 sec\n      \t\tdownload cloud file; open paint; launch terminal; launch explorer [ if kterm , explorer are installed ]\n\n\
\t3. Click ' Lang ' key to switch input language:CN, EN, DE [ 'C', 'E', 'D' on 'Aus ┋ ⍰ ' button to show input State ]\n\n\
\t4. Click ' scro⤽cal ' button to show scrollbar,  slide square handle to relocate txt page or  enter a line number\n      \t\ttext input is not valid in this state,  when 'as' button checked, 'scro⤽cal' button switch to calculator\n\n\
\t5. Click ' pick↝rpl ' button to show precise selection panel ,  slide square handle to select  text block  in editor\n      \t\tclick  ' △ '  or  ' ▽ '  button to select lines;\tquintuple click square handle to select all of text\n\n\
\t6. Click button wich is marked with  ' ◂ '  /  ' ▸ '  symbol at middle left/right of UI,    to page up or page down \n\n\
\t7. Search : select certain text in editor, click  'find⟳kln'  to search, when search result is hilighted, click button\n      \t\ton 'fnxt⟲pic'  to find next ;   when select none, click 'find⟳kln' button again to reset search feature\n\n\
\t8. Replace : e.g. type 'a@*b' in txt editor and select them, click  'pick⤼rpl' ,  all of  'a'  will be replaced by  'b'┋\n\n\
\t9. Click button ' Aus ┋ ⍰ '  to quit the application, back to Kindle main UI .\n\n\n\
\t* If there is letter in input field, click ' ( ) ' key to send original letter to editor ;    click ' °_° '  key to clean input\n\n\
\t* When ' as ' button is checked, 1. click ' ? ' button to show Info ( time, wifi ... )    2. ' Save '  button = ' Save as '\n      \t\tin  ' Save as '  status, type a name in editor and selecte it,  click save button to ' save as ' current file")
        if self.lab_help_popup.winfo_ismapped():
            self.lab_help_popup.place_forget()
            self.lab_help_popup.config(image = '', text='')
            self.lab_help_popup.place_configure(x=6, y=0+7, width=1249, height=880+54)
            self.root.after(120, lambda : self.lab_help_popup.place_forget() )          # to clean screen pix
        else: self.lab_help_popup.place_configure(x=6, y=0+7, width=1249, height=880+54)     #970
#-0--------------------------------------------------------
    def butn_scrol_clicked(self):
        if self.as_var.get()==1 and self.main_tx.tag_ranges("sel"):     #
            blk_lst = ('self', 'rm', 'remove', 'import', '__', 'del', 'delete', 'builtins', '|', '&', '^', '~', '>>', '<<')
            expression = self.main_tx.selection_get()
            for bw in blk_lst :
                if bw in expression :return
            tmp_buf = expression.replace(' ', '')
            if len( filter(lambda y: y in tmp_buf, map(lambda x: '**'.join((x,x,'')), [str(x) for x in xrange(5,1024)]) ) ) > 0: return
            #---
            try :      # print new_expression
                new_expression = self.py27_Mathematical_expression_int2float(expression)
                self.main_tx.insert( tk.SEL_LAST, ''.join(('\n', str(eval(str(new_expression))))) )            #
                self.root.after(70,lambda:self.arrow_dwn_key(None))
                self.root.after(70,lambda:self.arrow_up_key(None))
            except :
                self.info_pop('illegal math\nexpression,skip!\npls correct.')
            return
        else:
            self.frm_pop_pckt.place_forget()
            self.tx_ipt_pinyin.delete(0, tk.END)
            if not self.frm_pop_scrl.winfo_ismapped():
                self.butn_scrol.config(font=('Sans','7','bold', 'underline', 'italic'))
                self.butn_pick_rpl.config(font=('Sans','7','bold'))
                self.frm_pop_pckt.place_forget()
                self.frm_pop_scrl.place_configure(x = 6, y = self.side_lst_bx_height + 95, width = 1249 , height = 80)
                self.frm_pop_scrl.tkraise()
                self.lne_nmb.set('')
                #---
                self.main_tx['yscrollcommand'] = self.scrlbr_main_vtkl.set
                self.root.after( 50, lambda : self.scrol_bar_main_tx.set(int(self.main_tx.yview()[0]*100)) )
                #---
                self.kbd.ipt_widget = self.spin_lns_ipt
                self.info_pop('type line-numb\n or slide handle')
            else :        # print self.main_tx.yview_moveto()
                self.butn_scrol.config(font=('Sans','7','bold'))
                self.frm_pop_scrl.place_forget()
                self.kbd.ipt_widget = self.tx_ipt_pinyin
                self.info_pop('hide scroll panel\ninput redirect\nto pinyin field')
                self.main_tx.tag_remove('highlight','1.0', tk.END)
            self.root.after(30, lambda : self.kbd.updata_kbd(self.kbd.shift_state, self.lang) )

    def scrol_bar_mapping(self, event=None): self.main_tx.yview_moveto(self.scrol_bar_main_tx.get()/100.0 )        #

    def spin_box_2lne_nmb_changed(self):
        if not self.lne_nmb.get(): return
        tmp_spin = self.spin_lns_ipt.get()      #get input char first
        set_ln_nmb = ''.join([xx for xx in self.lne_nmb.get() if xx in ('0','1','2','3','4','5','6','7','8','9')])
        self.lne_nmb.set(set_ln_nmb)
        if not set_ln_nmb : return
        if set_ln_nmb != tmp_spin : return      #if there is a illegal chr in spinbox
        self.root.after(2, lambda : self.main_tx.see( ''.join((str(int(set_ln_nmb)), '.1')) ) )
        self.root.after( 90, lambda : self.scrol_bar_main_tx.set(int(self.main_tx.yview()[0]*100)) )
        self.root.after(150, lambda : self.main_tx.see( ''.join((str(int(set_ln_nmb)), '.1')) ) )
#-2--------------------------------------------------------
    def butn_pick_rpl_clicked(self):
        crnt_ipt_sym=self.entry_ipt_var.get()
        if crnt_ipt_sym: self.slid_pick['label'] = crnt_ipt_sym
        else : self.slid_pick['label'] = ' '
        #---
        if self.main_tx.tag_ranges("sel") :     #for replacement
            slct_chr = self.main_tx.selection_get()
            if '@*' in slct_chr and len(slct_chr.split('@*', 1)[-1])>0 and len(slct_chr.split('@*', 1)[0])>0:
                crnt_indx = self.main_tx.index(tk.INSERT)
                repl_chr = slct_chr.split('@*', 1)
                #---                # self.main_tx.delete("%s-1c" % tk.INSERT, tk.INSERT)
                self.main_tx.delete( ("%s-" + str(len(repl_chr[1])+2) + "c") % self.main_tx.index(tk.SEL_LAST), self.main_tx.index(tk.SEL_LAST))
                #---
                all_tx = self.main_tx.get('1.0', tk.END)
                repl_tx=all_tx.replace(repl_chr[0],repl_chr[1]) if repl_chr[1] !='xxxdelxxx' else all_tx.replace(repl_chr[0],'')
                #---
                self.main_tx['undo']=0
                self.main_tx.delete('1.0', tk.END)
                self.main_tx.insert(tk.END, repl_tx)
                self.main_tx['undo']=1
                #---
                self.search_chr_action(repl_chr[1])
                self.main_tx.see(crnt_indx)
                self.info_pop('replacement is\ndone, pls check\nhilighted chars')
                return
        if not self.frm_pop_pckt.winfo_ismapped():
            self.frm_pop_scrl.place_forget()
            self.butn_scrol.config(font=('Sans','7','bold'))
            self.butn_pick_rpl.config(font=('Sans','7','bold', 'underline', 'italic'))
            self.kbd.ipt_widget = self.tx_ipt_pinyin
            self.frm_pop_pckt.place_configure(x = 6, y = self.side_lst_bx_height + 92, width = 1249 , height = 90)
            self.frm_pop_pckt.tkraise()
            self.info_pop('pick panel :\ncut, past\nlines selection')
            #---
            self.root.after(30, lambda : self.kbd.updata_kbd(self.kbd.shift_state, self.lang) )
            # self.main_tx.tag_remove('highlight','1.0', tk.END)
        else :
            self.frm_pop_pckt.place_forget()
            self.butn_pick_rpl.config(font=('Sans','7','bold'))
            self.info_pop('hide pick panel\nlines selection\nis deactivated')
        self.lab_help_popup.place_forget()
        self.root.after(100,lambda:self.main_tx.see(tk.INSERT))        #self.main_tx.see(tk.INSERT)

    def butn_copy_clicked(self):
        if self.as_var.get() == 0:   self.main_tx.event_generate("<<Cut>>")
        else : self.main_tx.event_generate("<<Copy>>")
        self.main_tx.see(tk.INSERT)

    def butn_past_clicked(self):
        self.main_tx.event_generate("<<Paste>>")
        self.main_tx.see(tk.INSERT)

    def butn_select_all_clicked(self, event=None): self.main_tx.tag_add('sel',1.0,tk.END)    #event_generate("<<SelectAll>>")

    def butn_nxt_line_clicked(self):
        crnt_cpp = self.main_tx.index(tk.SEL_FIRST) if self.main_tx.tag_ranges("sel") else self.main_tx.index(tk.INSERT)
        if not self.main_tx.tag_ranges("sel") or int(self.main_tx.index(tk.INSERT).split('.')[0]) >= int(self.main_tx.index(tk.SEL_LAST).split('.')[0]):
            self.arrow_dwn_key(None)
            self.main_tx.tag_add('sel',crnt_cpp, tk.INSERT )
            return
        if self.main_tx.tag_ranges("sel") and int(self.main_tx.index(tk.INSERT).split('.')[0]) <= int(self.main_tx.index(tk.SEL_LAST).split('.')[0]):
            org_cpp_s = self.main_tx.index(tk.SEL_FIRST)
            org_cpp_e = self.main_tx.index(tk.SEL_LAST)
            self.arrow_dwn_key(None)
            self.main_tx.tag_add('sel',org_cpp_s, org_cpp_e )
            self.main_tx.tag_remove('sel', org_cpp_s, tk.INSERT)

    def butn_pre_line_clicked(self):    #event_generate("<<SelectPrevLine>>")
        crnt_cpp = self.main_tx.index(tk.SEL_LAST) if self.main_tx.tag_ranges("sel") else self.main_tx.index(tk.INSERT)
        if not self.main_tx.tag_ranges("sel") or int(self.main_tx.index(tk.INSERT).split('.')[0]) <= int(self.main_tx.index(tk.SEL_FIRST).split('.')[0]):
            self.arrow_up_key(None)
            self.main_tx.tag_add('sel', tk.INSERT ,crnt_cpp)
            return
        if self.main_tx.tag_ranges("sel") and int(self.main_tx.index(tk.INSERT).split('.')[0]) >= int(self.main_tx.index(tk.SEL_FIRST).split('.')[0]):
            org_cpp_s = self.main_tx.index(tk.SEL_FIRST)
            org_cpp_e = self.main_tx.index(tk.SEL_LAST)
            self.arrow_up_key(None)
            self.main_tx.tag_add('sel',org_cpp_s, org_cpp_e )
            self.main_tx.tag_remove('sel', tk.INSERT, crnt_cpp)

    def slid_pick_released(self, event=None):
        self.slid_pick.set(0)
        self.main_tx.focus_force()

    def slid_pick_pressed(self, event=None):
        if self.main_tx.tag_ranges("sel") :     self.tx_sel_len = 1
        else:                                   self.tx_sel_len = 0

    def slid_pick_action(self,value):
        vlu = int(value)
        try :    #
            if self.tx_sel_len == 0:
                if vlu>0 :
                    if vlu>self.lzt_sld_vlu:        self.main_tx.tag_add('sel',  tk.INSERT , "%s+%dc" % (tk.INSERT, 1 ) )
                    elif vlu<self.lzt_sld_vlu:      self.main_tx.tag_remove('sel' , "%s+%dc" % (tk.INSERT, -1 ), tk.INSERT )
                    self.main_tx.mark_set(tk.INSERT, tk.SEL_LAST)    #unset(tk.INSERT)
                elif vlu<0 :
                    if vlu<self.lzt_sld_vlu:        self.main_tx.tag_add('sel', "%s+%dc" % (tk.INSERT, -1 ),  tk.INSERT )
                    elif vlu>self.lzt_sld_vlu:      self.main_tx.tag_remove('sel',  tk.INSERT, "%s+%dc" % (tk.INSERT, 1 ) )
                    self.main_tx.mark_set(tk.INSERT, tk.SEL_FIRST)    #unset(tk.INSERT)
            else :
                if self.main_tx.index(tk.INSERT) == self.main_tx.index(tk.SEL_FIRST):
                    if vlu > 0:
                        if vlu>self.lzt_sld_vlu:    self.main_tx.tag_remove('sel',  tk.SEL_FIRST, "%s+%dc" % (tk.INSERT, 1 ) )
                        elif vlu<self.lzt_sld_vlu:  self.main_tx.tag_add('sel', "%s+%dc" % ( tk.INSERT, -1), tk.INSERT )
                    elif vlu < 0:
                        if vlu<self.lzt_sld_vlu:    self.main_tx.tag_add('sel', "%s+%dc" % ( tk.INSERT, -1), tk.INSERT )
                        elif vlu>self.lzt_sld_vlu:  self.main_tx.tag_remove('sel',  tk.SEL_FIRST, "%s+%dc" % (tk.INSERT, 1 ) )
                    self.main_tx.mark_set(tk.INSERT, tk.SEL_FIRST)   #unset(tk.INSERT)
                if self.main_tx.index(tk.INSERT) == self.main_tx.index(tk.SEL_LAST):
                    if vlu > 0:
                        if vlu>self.lzt_sld_vlu:    self.main_tx.tag_add('sel',  tk.SEL_LAST, "%s+%dc" % (tk.INSERT, 1 ) )
                        elif vlu<self.lzt_sld_vlu:  self.main_tx.tag_remove('sel', "%s+%dc" % ( tk.INSERT, -1), tk.INSERT )
                    if vlu < 0:
                        if vlu<self.lzt_sld_vlu:    self.main_tx.tag_remove('sel', "%s+%dc" % ( tk.INSERT, -1), tk.INSERT )
                        elif vlu>self.lzt_sld_vlu:self.main_tx.tag_add('sel',  tk.SEL_LAST, "%s+%dc" % (tk.INSERT, 1 ) )
                    self.main_tx.mark_set(tk.INSERT, tk.SEL_LAST)    #unset(tk.INSERT)
            self.lzt_sld_vlu=vlu
        except : pass
#-4------------------------------------#
    def dispatch_input_2Language(self):
        crnt_ipt_sym=self.entry_ipt_var.get()
        if crnt_ipt_sym: self.slid_pick['label'] = crnt_ipt_sym
        else: self.slid_pick['label'] = ' '
        #---
        if crnt_ipt_sym in self.redrct_sym:
            self.main_tx.insert(tk.INSERT, crnt_ipt_sym)
            self.tx_ipt_pinyin.delete(0, tk.END)
            self.slid_pick['label'] = ' '
            return
        elif len(crnt_ipt_sym)>1 and crnt_ipt_sym[-1] in self.redrct_sym :
            self.main_tx.insert(tk.INSERT, crnt_ipt_sym)
            self.tx_ipt_pinyin.delete(0, tk.END)
            self.slid_pick['label'] = ' '
            return                      #
        self.tx_ipt_kill_after()        #for pinyin input delay to optimize power consumption
        self.tx_ipt_timer_id = self.root.after(self.input_click_delay, self.tx_ipt_reaction_delay)    #---!!!386

    def tx_ipt_reaction_delay(self):
        inpt_stt_dic = {'CN':self.setup_candidate_4CN, 'EN':self.setup_candidate_4EN_DE, 'DE':self.setup_candidate_4EN_DE }
        inpt_stt_dic.get(self.lang)()    #---!!!

    def tx_ipt_kill_after(self):
        if self.tx_ipt_timer_id :
            self.root.after_cancel(self.tx_ipt_timer_id)
            self.tx_ipt_timer_id = None

    def setup_candidate_4CN(self):
        crnt_piny=self.entry_ipt_var.get().strip().lower()
        crnt_piny=crnt_piny.replace(u'ü','').replace(u'ö','').replace(u'ä','').replace(u'ß','')
        try :#>1        # self.rslt_wd_lst=()
            if len(crnt_piny)>0:self.rslt_wd_lst=tuple(self.piyipt.guess_words(crnt_piny))
        except:print('pyimg error! function: setup_candidate_4CN')
        if len(self.rslt_wd_lst)<1 :
            self.set_default_candidate_wds()
            return
        for xx in xrange(9):
            if xx >= len(self.rslt_wd_lst): continue             #width=len(self.rslt_wd_lst[xx])*3
            self.radio_butn_lst[xx].config(  font=('Sans','7','normal'),wraplength=96, width=5 , padx=6,justify= 'center', text=self.rslt_wd_lst[xx], value=self.rslt_wd_lst[xx] )
        self.lzt_pge_nmb = 0
        self.top_flg = 0

    def setup_candidate_4EN_DE(self):
        crnt_ipt=self.entry_ipt_var.get().strip().lower()
        if len(crnt_ipt)<1:return       #
        lang_dic_vlu = []
        if self.lang == 'EN' : lang_dic_vlu = self.english_word_dic
        if self.lang == 'DE' : lang_dic_vlu = self.german_word_dic
        crnt_word=crnt_ipt.strip().lower()
        self.rslt_wd_lst=[]
        append_cnd_word=self.rslt_wd_lst.append
        if '^' not in crnt_word :
            for ii in lang_dic_vlu :
                if ii.startswith(crnt_word) and ii not in self.rslt_wd_lst:
                    append_cnd_word(ii)
                    if len(self.rslt_wd_lst)>64 : break
        else :
            buf_str=[x.strip() for x in crnt_word.split('^') if len(x)>0]
            if len(buf_str)<2:return
            for ii in lang_dic_vlu :
                if len(buf_str)<3:
                    if buf_str[0] in ii and buf_str[1] in ii and ii not in self.rslt_wd_lst:
                        append_cnd_word(ii)
                        if len(self.rslt_wd_lst)>64 : break
                else :
                    if buf_str[0] in ii and buf_str[1] in ii and buf_str[2] in ii and ii not in self.rslt_wd_lst:
                        append_cnd_word(ii)
                        if len(self.rslt_wd_lst)>64 : break
        if len(self.rslt_wd_lst)<1:
            self.set_default_candidate_wds()
            return
        for xx in xrange(9):
            if xx >= len(self.rslt_wd_lst): continue    #, width=len(self.rslt_wd_lst[xx])*1
            self.radio_butn_lst[xx].config( font=('Sans','5','normal'), wraplength=90, width=8, padx=0, justify= 'center', text=self.rslt_wd_lst[xx], value=self.rslt_wd_lst[xx] )
        self.lzt_pge_nmb = 0
        self.top_flg = 0

    def set_default_candidate_wds(self):
        if self.tx_ipt_timer_id:
            self.root.after_cancel(self.tx_ipt_timer_id)
            self.tx_ipt_timer_id = None
        if self.lang == 'CN':
            for xx in xrange(9): self.radio_butn_lst[xx].config(font=('Sans','7','normal'), wraplength=96, width=5 , padx=6, justify= 'center')
        else:
            for xx in xrange(9): self.radio_butn_lst[xx].config(font=('Sans','5','normal'), wraplength=90, width=8 , padx=0, justify= 'center')
        for xx in xrange(9): self.radio_butn_lst[xx].config(text=self.dft_cndt_dic[self.lang][xx], value= str(self.dft_cndt_dic[self.lang][xx]))
        self.lzt_pge_nmb = 0
        self.top_flg = 0

    def rad_butn_candidated_word_clicked(self):
        x= self.rad_butn_var.get() if self.lang == 'CN' else ''.join((self.rad_butn_var.get(),' '))
        self.main_tx.insert(tk.INSERT, x)
        self.main_tx.focus_force()
        self.main_tx.see(tk.INSERT)             # self.main_tx.see(self.main_tx.index(tk.INSERT))
        self.tx_ipt_pinyin.delete(0,tk.END)
        self.rslt_wd_lst = []
        self.set_default_candidate_wds()        # self.ipt_widget.focus_lastfor()
        self.main_tx.event_generate('<Left>')
        self.main_tx.event_generate('<Right>')  #--- seprt undo segment
#-5--------------------------------------------------------
    def butn_fnxt_img_clicked(self):
        al_hilght = self.main_tx.tag_ranges('highlight')    # pid = os.getpid()
        if not al_hilght :                                  #------------to check picture
            self.check_mPs_info()
            return #
        #---
        if self.as_var.get()==1:    self.fnxt_idx = self.fnxt_idx -2 #
        else : self.fnxt_idx = self.fnxt_idx +2 if self.fnxt_idx < len(al_hilght)-2 else 0
        #---
        self.main_tx.see(al_hilght[self.fnxt_idx])
        self.main_tx.mark_set(tk.INSERT, al_hilght[self.fnxt_idx])        #unset(tk.INSERT)
        self.lab_page_dwn['text'] = ''.join((u'*  page dw   ▶\nfind next is\nactivated\nfnxt idx : ', str(self.fnxt_idx/2+1), '/', str(len(al_hilght)/2-0)))

    def butn_find_cls_clicked(self):        # self.root.geometry( "1072x1448+0+0"  )
        self.fnxt_idx = 0
        if not self.main_tx.tag_ranges("sel") :
            self.main_tx.tag_remove('highlight','1.0', tk.END)
            if "highlight" in self.main_tx.tag_names(): self.main_tx.tag_delete("highlight")
            self.info_pop('search is\ndeactivated,\nresult is cleaned')
            return
        skey_wd = self.main_tx.selection_get()
        self.search_chr_action(skey_wd)
        result_count = str((len(self.main_tx.tag_ranges('highlight')))/2)
        self.info_pop('search is\nactivated,\nresult is hilighted')

    def search_chr_action(self,skey_wd):
        if "highlight" in self.main_tx.tag_names(): self.main_tx.tag_delete("highlight")
        kwd_len = len(skey_wd)
        idx_s = "1.0"
        while 1:
            idx_s = self.main_tx.search(skey_wd, idx_s, nocase=1, stopindex='end')
            if idx_s:
                idx_e = self.main_tx.index("%s+%dc" % (idx_s, kwd_len))
                self.main_tx.tag_add("highlight", idx_s, idx_e)
                self.main_tx.tag_config("highlight", background="grey50")
                idx_s = idx_e
            else:
                self.main_tx.tag_remove('sel','1.0', tk.END)
                return
#-6--------------------------------------------------------
    def page_up_down_clicked(self, typ):        #typ is 'dw'  'up'
        if not self.tx_ipt_pinyin.get() :       #
            crnt_idx = self.main_tx.index(tk.INSERT)
            if typ == 'dw' :    self.main_tx.yview_scroll(1,tk.PAGES)
            else :              self.main_tx.yview_scroll(-1,tk.PAGES)
            self.main_tx.mark_set(tk.INSERT,"@%d,%d" % (0,20))      #
            self.main_tx.insert(tk.INSERT, '')                      #
            self.main_tx.mark_set(tk.INSERT, crnt_idx)
            self.lab_page_dwn['text'] = ''.join( (u'*  page dw   ▶\npage location :\n',("%.2f" % (self.main_tx.yview()[0]*100)),'%', '\nLine No.: ', self.main_tx.index( "@%d,%d" % (0, 0) ).split('.')[0]) )
            #---
            if self.frm_pop_scrl.winfo_viewable() :
                self.root.after( 90, lambda : self.scrol_bar_main_tx.set(int(self.main_tx.yview()[0]*100)) )
            #---
        else :                  # page up down for result words
            pg_count = int(len(self.rslt_wd_lst)/9) if len(self.rslt_wd_lst)%9==0 else int(len(self.rslt_wd_lst)/9)+1
            if typ == 'dw' :
                if self.top_flg == 0 and self.lzt_pge_nmb ==0 :    self.lzt_pge_nmb = 0
                if self.top_flg == 0 : self.lzt_pge_nmb = self.lzt_pge_nmb + 1
                self.top_flg = 1
                if self.lzt_pge_nmb>=pg_count :
                    self.info_pop('to page down\neditor,clean\ninput field first')
                    return      #or self.lzt_pge_nmb<0
            else:               #up
                self.lzt_pge_nmb = self.lzt_pge_nmb - 1 if self.top_flg ==0 else self.lzt_pge_nmb - 2
                self.top_flg = 0
                if self.lzt_pge_nmb<0:
                    self.lzt_pge_nmb = 0
                    self.info_pop('to page up\neditor,clean\ninput field first')
                    return
            for idx, bb in enumerate(self.radio_butn_lst):
                crnt_wd_idx = self.lzt_pge_nmb*9 + idx
                if crnt_wd_idx >= len(self.rslt_wd_lst) or crnt_wd_idx < 0: bb.config(text='...', value='')
                else : bb.config(text=self.rslt_wd_lst[crnt_wd_idx],value=self.rslt_wd_lst[crnt_wd_idx] )
            if typ == 'dw' : self.lzt_pge_nmb = self.lzt_pge_nmb + 1 #if self.top_flg ==1 else self.lzt_pge_nmb +2

    def butn_open_clicked(self) :
        open_lst_sze = tuple([int(x) for x in self.lst_bx_open.winfo_geometry().split('+')[0].split('x')])
        hfwd_lst_sze = tuple([int(x) for x in self.lst_bx_hfwd.winfo_geometry().split('+')[0].split('x')])
        scrl_float_bar_vis = self.frm_pop_scrl.winfo_viewable() + self.frm_pop_pckt.winfo_viewable()
        # print(scrl_bar_hgh, scrl_bar_hgh)
        if hfwd_lst_sze[0] > 1 : self.lst_bx_hfwd.place_configure(x = 1068, y = 2+7, width = 0, height = self.side_lst_bx_height)
        if  open_lst_sze[0] > 1 :
            self.main_tx.config(wrap='word')
            self.lst_bx_open.place_configure(x = 6+50, y = 0+7, width = 0, height = self.side_lst_bx_height)
            #---
            self.main_tx.place_configure(x = 6, y = 0+7, width =1249, height =self.side_lst_bx_height)
            #---
            self.butn_open['text'] = 'Open'
            self.bkmrk_flg=0
            self.lab_page_dwn['text'] = ''.join( (u'*  page dw   ▶\npage location :\n',("%.2f" % (self.main_tx.yview()[0]*100)),'%', '\nLine No.: ', self.main_tx.index( "@%d,%d" % (0, 0) ).split('.')[0]) )
        else :
            self.main_tx.config(wrap='none')
            self.lst_bx_open.place_configure(x = 6+50, y = 0+7, width = 300, height =self.side_lst_bx_height)
            #---
            self.main_tx.place_configure(x = 304, y = 0+7, width = 1249-298, height =self.side_lst_bx_height)
            #---
            self.info_pop(u'click " ↹ Slide "\nto close\nleft slide bar')
            self.butn_open['text'] = '↹ Slide'
            self.butn_hfwd['text'] = 'Hfwd'
        self.lab_help_popup.place_forget()
        self.fill_open_files_list()
        self.main_tx.tag_remove('highlight','1.0', tk.END)
        self.en_cn_ui_exchange(''.join(('ui_lang=',self.ui_lang)))

    def fill_open_files_list(self):
        self.lst_bx_open.delete(0,tk.END)        # self.lst_bx_open.insert(tk.END, 'File/Browser')
        file_not_comp_formt_set = ('.jpg','.tif','.png','.gif','.bmp','.xpm','.mov','.avi','.wav','.mp3','.rar','.zip','.pdf','.doc','.rtf','.ppt','.azw','.mps')
        for ff in os.listdir(self.prj_pth_txt_odn)[::-1]:
            if os.path.isfile( ''.join((self.prj_pth_txt_odn, ff)) ) and ff[-4:].lower() not in file_not_comp_formt_set and ff[-5:].lower() not in ('.mobi','.epub','.azw3','.xlsx','.docx','.pptx','.pptm'):
                if ff=='cloud_lnk.ini' : continue
                self.lst_bx_open.insert(tk.END, ff.decode('utf-8'))
        if 'cloud_lnk.ini' in os.listdir(self.prj_pth_txt_odn) : self.lst_bx_open.insert(tk.END, 'cloud_lnk.ini')
        if  os.path.isfile('/mnt/us/documents/My Clippings.txt') : self.lst_bx_open.insert(tk.END, 'Doc::My Clippings.txt')
        self.lst_bx_open.insert(tk.END, ' ')
#---
    def open_lst_item_clicked(self, event=None):
        if self.bkmrk_flg==0:       #open file mode
            if self.check_file_md5()!=self.lzt_md5 or self.main_tx.edit_modified()== 1:
                quit_id = self.root.after( 420000, lambda : self.root.destroy() )
                rslt = tkmsgbx_ask_yes_no('L:D_N:dialog_ID:PySide5','Current file is not saved\n文件尚未存盘, 是否开启新文件 ?\n\nDo you want to open new file ?',icon='info')
                if not rslt :
                    self.root.after_cancel(quit_id)
                    return          #
                else : self.root.after_cancel(quit_id)
            crnt_shnm = self.lst_bx_open.get(self.lst_bx_open.curselection())
            #---
            if crnt_shnm and crnt_shnm == 'Doc::My Clippings.txt' :
                my_clippings_pth = '/mnt/us/documents/My Clippings.txt'
                self.save_scroll_bar_value()
                self.open_tx_file_action(my_clippings_pth)
                #
                return
            #---
            if not crnt_shnm or not os.path.isfile( ''.join((self.prj_pth_txt_odn, crnt_shnm)) ): return
            if os.path.getsize( ''.join((self.prj_pth_txt_odn, crnt_shnm)) )>12288000: #32768000: 32Mb   #10240000: 10Mb
                self.lab_page_up['text'] = ''.join((u'◀   page up  *\nthe txt file is too\n larger to open\n( >12Mb ), skip :', crnt_shnm))
                self.info_pop('the file is too\n larger to open\n( >12Mb ),skip')
                return
            self.save_scroll_bar_value()
            #
            if self.frm_pop_scrl.winfo_ismapped():
                self.butn_scrol_clicked()
                self.open_tx_file_action( ''.join((self.prj_pth_txt_odn, crnt_shnm)) )
                self.main_tx.focus_force()
                self.butn_scrol_clicked()
                self.root.after(1010, lambda : self.kbd.updata_kbd(self.kbd.shift_state, self.lang) )
                # if self.frm_pop_scrl.winfo_viewable() :
                self.root.after( 90, lambda : self.scrol_bar_main_tx.set(int(self.main_tx.yview()[0]*100)) )
            else:
                self.open_tx_file_action( ''.join((self.prj_pth_txt_odn, crnt_shnm)) )
                self.main_tx.focus_force()
        else :                                                      #
            #
            crnt_bkmktx = self.lst_bx_open.get(self.lst_bx_open.curselection())
            if self.bkmrk_sprt not in crnt_bkmktx : return          #self.bkmrk_sprt='##%'
            #---
            crnt_active_idx = int(self.lst_bx_open.curselection()[0])
            al_itm_lsbx = self.lst_bx_open.get('0', tk.END)
            bmk_idx = 0
            for ii in al_itm_lsbx[:crnt_active_idx+1]:
                if ii == crnt_bkmktx : bmk_idx = bmk_idx +2
            if bmk_idx>0:bmk_idx = bmk_idx -1
            #---
            self.main_tx.tag_remove('highlight','1.0', tk.END)
            self.search_chr_action(crnt_bkmktx)
            al_hilght = self.main_tx.tag_ranges('highlight')
            if not al_hilght :  return
            self.main_tx.see(al_hilght[bmk_idx])                    #
            if self.frm_pop_scrl.winfo_viewable() :
                self.root.after( 90, lambda : self.scrol_bar_main_tx.set(int(self.main_tx.yview()[0]*100)) )

    def butn_bkmrk_clicked(self):
        open_lst_sze = tuple([int(x) for x in self.lst_bx_open.winfo_geometry().split('+')[0].split('x')])
        if self.bkmrk_flg==0 and open_lst_sze[0] > 1 :
            self.lst_bx_open.place_configure(x = 6+50, y = 0+7, width = 0, height = self.side_lst_bx_height)
            self.main_tx.place_configure(x = 6, y = 0+7, width =1249, height =self.side_lst_bx_height)
            self.main_tx.config(wrap='word')
            self.butn_open['text'] = 'Open'
        self.root.after( 90, self.book_mark_slidbar_action  )
        self.main_tx.tag_remove('highlight','1.0', tk.END)
        self.en_cn_ui_exchange(''.join(('ui_lang=',self.ui_lang)))

    def book_mark_slidbar_action(self):
        open_lst_sze = tuple([int(x) for x in self.lst_bx_open.winfo_geometry().split('+')[0].split('x')])
        hfwd_lst_sze = tuple([int(x) for x in self.lst_bx_hfwd.winfo_geometry().split('+')[0].split('x')])
        #
        if hfwd_lst_sze[0] > 1 : self.lst_bx_hfwd.place_configure(x = 1068, y = 2+7, width = 0, height = self.side_lst_bx_height)
        if  open_lst_sze[0] > 1 :
            self.main_tx.config(wrap='word')
            self.lst_bx_open.place_configure(x = 6+50, y = 0+7, width = 0, height = self.side_lst_bx_height)
            self.main_tx.place_configure(x = 6, y = 0+7, width =1249, height =self.side_lst_bx_height)
            #---
            self.butn_open['text'] = 'Open'
            self.bkmrk_flg=0
            self.lab_page_dwn['text'] = ''.join( (u'*  page dw   ▶\npage location :\n',("%.2f" % (self.main_tx.yview()[0]*100)),'%', '\nLine No.: ', self.main_tx.index( "@%d,%d" % (0, 0) ).split('.')[0]) )
        else :
            self.main_tx.config(wrap='none')
            self.lst_bx_open.place_configure(x = 6+50, y = 0+7, width = 300, height =self.side_lst_bx_height)
            self.main_tx.place_configure(x = 304, y = 0+7, width = 1249-298, height =self.side_lst_bx_height)
            #---
            self.info_pop(u'click " ↹ Slide "\nto close\nleft slide bar')
            self.butn_open['text'] = '↹ Slide'
            self.butn_hfwd['text'] = 'Hfwd'
            self.bkmrk_flg=1

        self.lab_help_popup.place_forget()
        self.fill_book_mark_list()
        self.en_cn_ui_exchange(''.join(('ui_lang=',self.ui_lang)))

    def fill_book_mark_list(self):          #self.bkmrk_sprt = '##%'
        self.lst_bx_open.delete(0,tk.END)
        all_tx = self.main_tx.get('1.0', tk.END)
        if self.bkmrk_sprt not in all_tx: return
        bookmark_lst = ['{}{}'.format(self.bkmrk_sprt, x[:12]) for x in all_tx.split(self.bkmrk_sprt) if len(x)>0][1:]
        for bmk in bookmark_lst : self.lst_bx_open.insert(tk.END, bmk.decode('utf-8'))
        self.lst_bx_open.insert(tk.END, ' ')
#---
    def open_tx_file_action(self,file_nm):
        self.main_tx.edit_reset()
        self.main_tx['undo']=0              #clean undo stacks
        self.convert_win_endline_2nix_endline(file_nm)
        with cds_open(file_nm,'r',encoding='utf-8',errors='ignore') as rid: buf_str=rid.readlines()
        self.main_tx.delete(1.0,tk.END)
        for ii in buf_str :
            try : self.main_tx.insert(tk.INSERT,ii)
            except : pass
        self.main_tx['undo']=1
        self.crnt_file_nm = file_nm
        self.lzt_md5 = self.check_file_md5()
        self.main_tx.edit_modified(0)       #set file modify flag 0 (not changed)
        #---
        self.mps_pos_len_dic = {}
        if os.path.isdir(self.prj_pth_mps_odn) :    #for skip doc::myclippings.txt
            for cf in os.listdir(self.prj_pth_mps_odn):os.remove(''.join((self.prj_pth_mps_odn,cf)))
        #---
        file_shnm = os.path.basename(file_nm) if len(os.path.basename(file_nm)) < 16 else ''.join((os.path.basename(file_nm)[:7], '...', os.path.basename(file_nm)[-7:]))
        self.lab_page_up['text'] = ''.join((u'◀   page up  *\nfile is opened:\n', file_shnm))
        self.info_pop(''.join(('file is opened :\n', os.path.basename(file_nm))))
        #---
        self.load_scroll_bar_pos(file_nm)

    def check_file_md5(self):  return len(self.main_tx.get("1.0","end-1c"))  # toHex
    def butn_hfwd_clicked(self):
        open_lst_sze = tuple([int(x) for x in self.lst_bx_open.winfo_geometry().split('+')[0].split('x')])
        hfwd_lst_sze = tuple([int(x) for x in self.lst_bx_hfwd.winfo_geometry().split('+')[0].split('x')])
        scrl_float_bar_vis = self.frm_pop_scrl.winfo_viewable() + self.frm_pop_pckt.winfo_viewable()
        if open_lst_sze[0] > 1 : self.lst_bx_open.place_configure(x = 6, y = 0+7, width = 0, height = self.side_lst_bx_height)
        if  hfwd_lst_sze[0] > 1 :
            self.main_tx.config(wrap='word')
            self.lst_bx_hfwd.place_configure(x = 1068, y = 0+7, width = 0, height = self.side_lst_bx_height)
            #---
            self.main_tx.place_configure(x = 6, y = 0+7, width =1249, height =self.side_lst_bx_height)
            #---
            self.butn_hfwd['text'] = 'Hfwd'
            self.lab_page_dwn['text'] = ''.join( (u'*  page dw   ▶\npage location :\n',("%.2f" % (self.main_tx.yview()[0]*100)),'%', '\nLine No.: ', self.main_tx.index( "@%d,%d" % (0, 0) ).split('.')[0]) )
        else :
            self.main_tx.config(wrap='none')
            self.lst_bx_hfwd.place_configure(x = 1249-235, y = 0+7, width = 225, height = self.side_lst_bx_height)  #+6
            #---
            self.main_tx.place_configure(x = 6, y = 0+7, width = 1249-225, height =self.side_lst_bx_height)
            #---
            self.info_pop(u'click " Slide ↹ "\nto close\nright slide bar')
            self.butn_hfwd['text'] = 'Slide ↹'
            self.butn_open['text'] = 'Open'
            self.bkmrk_flg=0
            #----
        self.lab_help_popup.place_forget()
        self.fill_hfwd_fctn_list()
        self.en_cn_ui_exchange(''.join(('ui_lang=',self.ui_lang)))

    def fill_hfwd_fctn_list(self):
        self.lst_bx_hfwd.delete(0,tk.END)
        hfwd_fctn_lst_pth=''.join((self.prj_pth_config,'hfwd_lst.ini'))
        try :    #
            if os.path.isfile(hfwd_fctn_lst_pth):
                with cds_open(hfwd_fctn_lst_pth,'r',encoding='utf8') as rid:  buf=rid.read().split('-*:%:*-')[:-1]
                for ii in buf:
                    tmp = ii
                    if ii == u'Ui_lang_CN:界面':
                        if self.ui_lang == 'cn':  tmp = u'Ui_lang_EN:界面'
                    if ii == u'BgLED__00:背光':
                        if int(os.popen('lipc-get-prop com.lab126.powerd flIntensity').read())==0: tmp = u'BgLED__09:背光'
                        elif int(os.popen('lipc-get-prop com.lab126.powerd flIntensity').read())==21: tmp = u'BgLED__09:背光'
                    self.lst_bx_hfwd.insert(tk.END, str(tmp).decode('utf8'))
        except : print('can not load hfwd !')           # self.lst_bx_hfwd.itemconfig(3,bg='red')

    def hfwd_lst_item_clicked(self, event=None):

        crnt_cmd = self.lst_bx_hfwd.get(self.lst_bx_hfwd.curselection())
        if not crnt_cmd: return
        if   crnt_cmd==u'BgLED__00:背光':
            os.popen("lipc-set-prop com.lab126.powerd flIntensity 0")
            updata_idx = self.lst_bx_hfwd.curselection()
            self.lst_bx_hfwd.delete(updata_idx)
            self.lst_bx_hfwd.insert(updata_idx, u'BgLED__09:背光')
        elif crnt_cmd==u'BgLED__09:背光':            #
            os.popen("lipc-set-prop com.lab126.powerd flIntensity 9")
            updata_idx = self.lst_bx_hfwd.curselection()
            self.lst_bx_hfwd.delete(updata_idx)
            self.lst_bx_hfwd.insert(updata_idx, u'BgLED__16:背光')
        elif crnt_cmd==u'BgLED__16:背光':            #
            os.popen("lipc-set-prop com.lab126.powerd flIntensity 16")
            updata_idx = self.lst_bx_hfwd.curselection()
            self.lst_bx_hfwd.delete(updata_idx)
            self.lst_bx_hfwd.insert(updata_idx, u'BgLED__00:背光')
        elif crnt_cmd == u'Ui_lang_CN:界面':
            self.en_cn_ui_exchange('ui_lang=cn')
            updata_idx = self.lst_bx_hfwd.curselection()
            self.lst_bx_hfwd.delete(updata_idx)
            self.lst_bx_hfwd.insert(updata_idx, u'Ui_lang_EN:界面')
        elif crnt_cmd == u'Ui_lang_EN:界面':
            self.en_cn_ui_exchange('ui_lang=en')
            updata_idx = self.lst_bx_hfwd.curselection()
            self.lst_bx_hfwd.delete(updata_idx)
            self.lst_bx_hfwd.insert(updata_idx, u'Ui_lang_CN:界面')
        elif crnt_cmd==u'BgLED__21:手电':                 #
            os.popen("lipc-set-prop com.lab126.powerd flIntensity 21")
            if self.lst_bx_hfwd.get(0)==u'BgLED__00:背光':
                self.lst_bx_hfwd.delete(0)
                self.lst_bx_hfwd.insert(0, u'BgLED__09:背光')
        elif crnt_cmd==u'Wifi_switch:网络':
            if self.wifi == 0:
                os.popen("lipc-set-prop com.lab126.cmd wirelessEnable 1")    # os.popen("lipc-set-prop com.lab126.quickactions toggleAirplaneMode enable")
                self.wifi =1
                self.info_pop('Wi-Fi is :\nOn')
            else :
                os.popen("lipc-set-prop com.lab126.cmd wirelessEnable 0")    # os.popen("lipc-set-prop com.lab126.quickactions toggleAirplaneMode enable")
                self.wifi =0
                self.info_pop('Wi-Fi is :\nOff')
        elif crnt_cmd==u'Ssht__i5sec:截屏':               #
            self.lab_page_dwn['text'] = u'*  page dw   ▶\nsscreenshot\nin 5 seconds'
            self.root.after(7100,lambda:os.popen("screenshot") )
            self.root.after(3072, lambda: self.info_right_tips(u'screenshot\nin 3 seconds') )
            self.root.after(4096, lambda: self.info_right_tips(u'screenshot\nin 2 seconds') )
            self.root.after(5120, lambda: self.info_right_tips(u'screenshot\nin 1 seconds') )
            self.root.after(7168, lambda: self.info_right_tips(u'screenshot is\ndone, Pls\ncheck root dir') )
            self.root.after(10240, lambda: self.info_right_tips(u' ') )
        elif crnt_cmd==u'Ssvr_switch:屏保':
            if self.ssvr==1:
                os.popen("lipc-set-prop com.lab126.powerd preventScreenSaver 0")
                self.ssvr=0
                self.info_pop('screensaver\nis : On')
            else:
                os.popen("lipc-set-prop com.lab126.powerd preventScreenSaver 1")
                self.ssvr=1
                self.info_pop('screensaver\nis : Off')
        elif crnt_cmd==u'EXPLoreR:理文件':      # subprocess.call("/mnt/us/extensions/explorer/bin/explorer.sh &")
            os.popen("exec /mnt/us/extensions/explorer/bin/explorer.sh &")
        elif crnt_cmd==u'TeRMinaL:命令行':      # subprocess.call("/mnt/us/extensions/explorer/bin/kterm.sh &")
            rslt = tkmsgbx_ask_yes_no(u'L:D_N:dialog_ID:PySide6','\nDo you want to open Linux command line ?\n打开Linux命令行 ?\n\n\n     * how to quit Linux command line:\n       touch screen with two fingers,\n       click "Quit" .\n\n     * 关于如何退出命令行, 返回n31_kte:\n       用两个手指同时触碰屏幕, 点"Quit".', icon='info')
            if rslt:
                os.popen("exec /mnt/us/extensions/kterm/bin/kterm.sh &")
        elif crnt_cmd==u'N31>Paint: ※涂画':     # subprocess.call("/mnt/us/extensions/explorer/bin/kterm.sh &")🔭✻
            self.butn_hfwd_clicked()
            self.paint = TK_PAINT(parent=self)
            self.paint.place( x=6, y=0, width = 1249 )
            self.root.after(120, lambda : self.kbd.updata_kbd(self.kbd.shift_state, self.lang) )
        elif crnt_cmd==u'Embed-pic:☹嵌图':
            rslt = tkmsgbx_ask_yes_no(u'L:D_N:dialog_ID:PySide9','\nDo you want to embed image into txt ?\n在当前文本中嵌入图片 ?\n\n\n    1. copy the images  ( 1.gif, 2.gif ... )   to\n        .../mps_buffer/\n    2. mark text line with: (*pic=1:-9*)\n\n\n    1. 复制待嵌入的gif图片 ( 1.gif, 2.gif ... )\n        至.../mps_buffer/\n    2. 在需要嵌图片的文本行插入:\n        (*pic=1:-9*)', icon='info')
            if rslt:
                self.create_embed_img_mps_file()
        elif crnt_cmd==u'Cloud>File:云文本':    #
            if int(os.popen('lipc-get-prop com.lab126.cmd wirelessEnable').read())==0:
                if self.as_var.get() == 1:
                    if self.main_tx['padx'] == 10:
                        self.main_tx.config(padx=100)
                        return
                    else :
                        self.main_tx.config(padx=10)
                        return
                else :
                    if str(os.popen('lipc-get-prop com.lab126.winmgr epdcMode').read()).strip(' \r\n') == 'Y8INV' :
                        os.popen("lipc-set-prop com.lab126.winmgr epdcMode Y8")
                        return
                    elif str(os.popen('lipc-get-prop com.lab126.winmgr epdcMode').read()).strip(' \r\n') == 'Y8':
                        os.popen("lipc-set-prop com.lab126.winmgr epdcMode Y8INV")
                        return
            else :
                cloud_file = n31_email.N31KTE_EMAIL(self.prj_pth_txt_odn, '', '', '')
                net_rslt = cloud_file.send_mail_chk('cloud')                    #
                if net_rslt ==1 :
                    self.info_pop('download txt\nfrom cloud,\nfile is updated')
                else :
                    self.info_pop('cloud config is\ncorrupted or NO\ninternet access')
                    if os.path.isfile( ''.join((self.prj_pth_config,'rplc_ssv.sh')) ) and self.as_var.get() == 1 :
                        os.popen("exec /mnt/us/extensions/n31_kte/config/rplc_ssv.sh &")      # to run extra shell change screensaver
                        self.info_pop('shell is\nexecuted\n/config/rplc_ssv.sh')
        #=========VVV

    def lang_key(self, key_chr):
        chng_lang_dic = {'CN':'EN','EN':'DE','DE':'CN',}
        self.lang=chng_lang_dic.get(self.lang)
        self.butn_aus['text'] = u' ┋ '.join(('Aus',self.lang[0]))   #---
        self.kbd.updata_kbd(self.kbd.shift_state, self.lang)        #---        # if self.lang != 'EN':
        self.tx_ipt_pinyin.delete(0,tk.END)
        self.set_default_candidate_wds()    #
        self.en_cn_ui_exchange(''.join(('ui_lang=',self.ui_lang)))
        #---

    def undo_key(self, key_chr):            #
        self.main_tx.event_generate("<<Undo>>")
        self.info_pop('undo\nis pressed !')

    def redo_key(self, key_chr):
        self.main_tx.event_generate("<<Redo>>")
        self.info_pop('redo\nis pressed !')

    def space_key(self, key_chr):  self.main_tx.insert(tk.INSERT, ' ')

    def bkspc_key(self, key_chr):    #
        if self.kbd.ipt_widget == self.spin_lns_ipt :       #
            self.spin_lns_ipt.delete(len(self.spin_lns_ipt.get())-1, tk.END)
            return
        if self.main_tx.tag_ranges("sel"):
            self.main_tx.delete(self.main_tx.index(tk.SEL_FIRST), self.main_tx.index(tk.SEL_LAST))
            return
        if not self.tx_ipt_pinyin.get() :    self.main_tx.delete("%s-1c" % tk.INSERT, tk.INSERT)
        else:    self.tx_ipt_pinyin.delete(len(self.tx_ipt_pinyin.get())-1, tk.END)

    def shift_key(self, key_chr=None):
        if self.kbd.shift_state == 0  : self.kbd.updata_kbd(1, self.lang)
        else :                          self.kbd.updata_kbd(0, self.lang)

    def enter_key(self, key_chr):
        if not self.tx_ipt_pinyin.get() :    self.main_tx.insert(tk.INSERT, '\n')
        else:
            self.radio_butn_lst[0].select()
            crnt_wd = self.rad_butn_var.get() if self.lang=='CN' else ''.join((self.rad_butn_var.get(), ' '))
            self.main_tx.insert(tk.INSERT, crnt_wd)             # self.main_tx.insert(tk.INSERT, self.rad_butn_var.get())
            self.radio_butn_lst[0].deselect()
            self.tx_ipt_pinyin.delete(0,tk.END)                 #---
            self.set_default_candidate_wds()
        self.main_tx.event_generate('<Left>')
        self.main_tx.event_generate('<Right>')                  #--- seprt undo segment

    def send_underscore_empty_del(self, key_chr):
        if self.frm_pop_scrl.winfo_viewable()==1:
            if self.main_tx.tag_ranges("sel"):
                self.main_tx.delete(self.main_tx.index(tk.SEL_FIRST), self.main_tx.index(tk.SEL_LAST))
                return
            self.main_tx.focus_force()
            self.main_tx.see(tk.INSERT)
            self.main_tx.delete("%s-1c" % tk.INSERT, tk.INSERT)
            return
        #---
        if not self.tx_ipt_pinyin.get() :    self.main_tx.insert(tk.INSERT, '_')
        else:  #
            self.tx_ipt_pinyin.delete(0,tk.END)
            self.set_default_candidate_wds()

    def db_bracket_key(self, key_chr):                      # db_less_key  db_parentheses_key  db_brace_key
        if self.frm_pop_scrl.winfo_viewable()== 1 and key_chr == '* * *' :
            self.main_tx.see(tk.INSERT)
            self.main_tx.insert(tk.INSERT, '***')
            return
        if self.frm_pop_scrl.winfo_viewable()== 1 : return
        #---
        if not self.tx_ipt_pinyin.get() :
            self.main_tx.insert(tk.INSERT, key_chr.replace(' ',''))
            crnt_pos = [int(x) for x in self.main_tx.index(tk.INSERT).split('.')]
            left_pos = '.'.join((str(crnt_pos[0]),str((crnt_pos[1]-1))))
            self.main_tx.mark_set(tk.INSERT,left_pos)       #unset(tk.INSERT)
        elif key_chr in ('(  )','[  ]',):
            self.main_tx.insert(tk.INSERT, self.tx_ipt_pinyin.get())
            self.tx_ipt_pinyin.delete(0,tk.END)
            self.set_default_candidate_wds()

    def dumy_key(self, key_chr):pass

    def arrow_lft_key(self, key_chr):
        self.main_tx.focus_force()
        self.main_tx.event_generate('<Left>')
        self.main_tx.see(tk.INSERT)
        self.main_tx.focus_force()

    def arrow_rht_key(self, key_chr):
        self.main_tx.focus_force()
        self.main_tx.event_generate('<Right>')
        self.main_tx.see(tk.INSERT)
        self.main_tx.focus_force()

    def arrow_up_key(self, key_chr):
        self.main_tx.focus_force()
        self.main_tx.event_generate('<Up>')
        self.main_tx.see(tk.INSERT)
        self.main_tx.focus_force()

    def arrow_dwn_key(self, key_chr):
        self.main_tx.focus_force()
        self.main_tx.event_generate('<Down>')
        self.main_tx.see(tk.INSERT)
        self.main_tx.focus_force()

    def load_scroll_bar_pos(self,crnt_file):
        if not crnt_file:return
        if not os.path.isfile(''.join((self.prj_pth_config,'scroll_bar_value.ini'))): return
        with cds_open(''.join((self.prj_pth_config,'scroll_bar_value.ini')),'r',encoding='utf-8') as rid:
            try : scrlbv_dic=eval(rid.readline())
            except : return
        scrolbar_v=scrlbv_dic.get(str(crnt_file).decode('utf8'))
        if not scrolbar_v: scrolbar_v="1.0"
        self.main_tx.mark_set(tk.INSERT,str(scrolbar_v))
        self.main_tx.see(scrolbar_v)
        self.main_tx.mark_set(tk.INSERT,"@%d,%d" % (0,20))
        self.main_tx.insert(tk.INSERT, '')     # self.main_tx.focus_force()

    def save_scroll_bar_value(self):
        if not self.crnt_file_nm:return
        if '\\' in self.crnt_file_nm or '{' in self.crnt_file_nm or '}' in self.crnt_file_nm or ':' in self.crnt_file_nm or ',' in self.crnt_file_nm or "'" in self.crnt_file_nm or '"' in self.crnt_file_nm :return
        if not os.path.isfile(''.join((self.prj_pth_config,'scroll_bar_value.ini'))) :
            with cds_open(''.join((self.prj_pth_config,'scroll_bar_value.ini')),'w',encoding='utf-8') as wid: wid.write('{}')
        with cds_open(''.join((self.prj_pth_config,'scroll_bar_value.ini')),'r',encoding='utf-8') as rid:
            try : scrlbv_dic=eval(rid.readline())
            except : return
        self.main_tx.focus_force()
        self.main_tx.mark_set(tk.INSERT,"@%d,%d" % (0,20))  #
        scrlbv_dic[unicode(str(self.crnt_file_nm))]=''.join((str(int(self.main_tx.index(tk.INSERT).split('.')[0])+8), '.0'))  #9
        with cds_open(''.join((self.prj_pth_config,'scroll_bar_value.ini')),'w',encoding='utf-8') as wid:
            wid.write('{')
            for kk, vv in scrlbv_dic.items():    wid.write("".join(["u'", str(kk), "'", ":", str(vv),","]))
            wid.write("u'init_x|x|x':0}")

    def info_lab_clicked(self):                         # akku = subprocess.call('gasgauge-info -c', shell=True)
        akku = os.popen('gasgauge-info -c').read().strip('\r\n ') if os.popen('gasgauge-info -c').read() else 'unk'
        if int(akku[:-1]) > 100 : akku = '100%'         #fix--- 102%
        ssvs = 'off' if int(os.popen('lipc-get-prop com.lab126.powerd preventScreenSaver').read())==1 else 'on'         #
        tx_cunt = len(self.main_tx.get("1.0","end-1c")) if self.main_tx.get("1.0","end-1c")  else 0                     #
        wifi_stt = 'on' if int(os.popen('lipc-get-prop com.lab126.cmd wirelessEnable').read())==1 else 'off'
        crnt_time = str(os.popen('date +%H:%M').read())

        inf_tx = ('Akku\n{}\n\nWi-Fi\n{}\n\nScnSv\n{}\n\ntxtcnt\n{}\n\n\n\n\nTime\n{}'.format(akku,wifi_stt,ssvs,tx_cunt,crnt_time))
        self.root.after(18000, lambda:self.lab_sys_info.config(text ='Akku\n{}\n\nWi-Fi\n{}\n\nScnSv\n{}\n\ntxtcnt\n{}\n\n\n\n\nTime\n{}'.format('...','...','...','...','...')))
        if self.ui_lang=='cn':
            inf_tx = inf_tx.replace('Akku',u'电量').replace('Wi-Fi',u'网络').replace('ScnSv',u'屏保').replace('txtcnt',u'字数').replace('Time',u'时间')
            self.root.after(18200, lambda:self.lab_sys_info.config(text =u'电量\n{}\n\n网络\n{}\n\n屏保\n{}\n\n字数\n{}\n\n\n\n\n时间\n{}'.format('...','...','...','...','...')))
        self.lab_sys_info['text']=inf_tx
        # if self.crnt_file_nm:   self.set_task_bar_info()

    def updated_keyboard_state(self):
        self.root.after(120, lambda : self.kbd.updata_kbd(self.kbd.shift_state, self.lang) )

    def py27_Mathematical_expression_int2float(self, ipt_exprsn='' ):
        #
        try: eval(ipt_exprsn)
        except :
            print('illegal mathematical experssion, skip!')
            return
        math_operator = frozenset((' ', '+', '-', '~', '*', '/', '//', '|', '&', '<', '>',  '=',  '!', ':', ',', '%', '^', '**', '[', ']', '(', ')', '{', '}', 'in', 'for', 'lambda', 'if', 'else', 'is', 'not', 'or', 'and', 'await', 'True', 'False', 'return'))
        int_uid2str_dic = {'0':'A', '1':'B', '2':'C', '3':'D', '4':'E', '5':'F', '6':'G', '7':'H', '8':'I', '9':'J' }
        #---
        mark_exprsn = ipt_exprsn[:]
        for buf_optr in math_operator :
            if buf_optr in ipt_exprsn : mark_exprsn = mark_exprsn.replace(buf_optr, '###')

        segmentation_lst = [ x.strip() for x in mark_exprsn.split('#') if x.strip()!='']
        int_lst, flt_lst = [], []
        for ii in segmentation_lst:
            try:
                if int(float(ii)) == float(ii):
                    if '.' in ii :  flt_lst.append(ii)
                    else :          int_lst.append(ii)
            except : pass
            try:
                if int(float(ii)) != float(ii) : flt_lst.append(ii)
            except : pass
        if len(int_lst) == 0 : return ipt_exprsn
        #===  mask range sgmnt VVV
        proxy_digital_dic={}
        mask_exprsn = ipt_exprsn[:]#
        range_mask_idx = [i for i in range(len(mask_exprsn)) if mask_exprsn.startswith('range', i)]
        msk_rplced_exp = ''
        if len(range_mask_idx)>0: #return
            mask_lst =[]
            for mm in range_mask_idx:
                end_flg = 0
                str_flg = 0
                for sdx, kk in enumerate( mask_exprsn[ mm + len('range'): ] ):
                    if kk=='(' :
                        str_flg = str_flg +1
                        end_flg = end_flg +1
                    elif kk==')': end_flg = end_flg -1
                    if str_flg>0 and end_flg == 0:
                        msk_buf = mask_exprsn[mm: mm + len('range') + sdx +1]
                        mask_lst.append(msk_buf)
                        break
            for msk in mask_lst :        # uid_int_str = [x for x in str(uuid.uuid4().int)]
                crnt_prxy = ''.join(map(lambda x: int_uid2str_dic[x], [x for x in str(uid4().int)]))
                msk_rplced_exp = mask_exprsn.replace(msk, crnt_prxy, 1)
                proxy_digital_dic[crnt_prxy] = msk
                mask_exprsn = msk_rplced_exp
        #===
        buf_exprsn = ipt_exprsn[:] if len(msk_rplced_exp)<8 else msk_rplced_exp[:]
        flt_rplced_exp = ''
        for flt in flt_lst :        # uid_int_str = [x for x in str(uuid.uuid4().int)]
            crnt_prxy = ''.join(map(lambda x: int_uid2str_dic[x], [x for x in str(uid4().int)]))
            flt_rplced_exp = buf_exprsn.replace(flt, crnt_prxy, 1)
            proxy_digital_dic[crnt_prxy] = flt
            buf_exprsn = flt_rplced_exp

        relay_exprsn = msk_rplced_exp[:] if len(msk_rplced_exp)>3 else ipt_exprsn[:]
        tmp_exprsn = flt_rplced_exp[:] if len(flt_lst) >0 else relay_exprsn[:]    #ipt_exprsn[:]
        int_rplced_exp = ''
        for dd in int_lst:
            int_rplced_exp = tmp_exprsn.replace(dd, dd+'.0', 1)
            crnt_prxy = ''.join(map(lambda x: int_uid2str_dic[x], [x for x in str(uid4().int)]))
            int_rplced_exp = int_rplced_exp.replace(dd+'.0',crnt_prxy, 1)
            proxy_digital_dic[crnt_prxy] = ''.join((dd,'.0'))
            tmp_exprsn= int_rplced_exp

        cache_exprsn = int_rplced_exp[:] #
        rslt_exp=''
        for kk, vv in proxy_digital_dic.iteritems():
            rslt_exp = cache_exprsn.replace(kk,vv,1)
            cache_exprsn = rslt_exp
        return rslt_exp

class N31_KTE_KBD(tk.Frame):
    __slots__ = ('butn_stndr_color', 'fctn_key_dic', 'ipt_widget', 'keysize', 'lang_state', 'lzt_butn_lst', 'parent', 'shift_state', 'sym_list' )
    def __init__(self, parent, ipt_widget, shift_state, lang_state, keysize=6):
        tk.Frame.__init__(self, takefocus=0)        #
        self.parent = parent
        self.ipt_widget = ipt_widget
        self.shift_state=shift_state
        self.lang_state=lang_state
        self.keysize = keysize
        self.sym_list = {}
        self.lzt_butn_lst = []
        self.butn_stndr_color = []
        self.fctn_key_dic={ 'Lang': self.parent.lang_key, 'undo': self.parent.undo_key, 'redo': self.parent.redo_key,'{ }': self.parent.db_bracket_key,'(  )': self.parent.db_bracket_key, '< >': self.parent.db_bracket_key, '‘ ’': self.parent.db_bracket_key,
                        '[  ]': self.parent.db_bracket_key,u' ▲ ': self.parent.arrow_up_key, u' ◀ ': self.parent.arrow_lft_key,u' ▶ ': self.parent.arrow_rht_key,u' ▼ ': self.parent.arrow_dwn_key,'S P A C E': self.parent.space_key,
                        'shift': self.parent.shift_key, 'Enter': self.parent.enter_key, u'░': self.parent.dumy_key, '° _ °': self.parent.send_underscore_empty_del,'< Bks': self.parent.bkspc_key, u'“ ”': self.parent.db_bracket_key,
                        '" "': self.parent.db_bracket_key,"' '": self.parent.db_bracket_key, '<<<=': self.parent.send_underscore_empty_del, '* * *': self.parent.db_bracket_key}  #
        self.config( border=0, borderwidth=0, relief='flat', highlightthickness=0,bg='white')
        self.mapping_kbd_symb(self.shift_state, self.lang_state)
        self.setup_kbd()        #----------

    def mapping_kbd_symb(self, shift_sst, lang_sst):
        if shift_sst==0 and lang_sst == 'CN':
            self.sym_list={'00nwrw':0,'01Lang':1.1,'021':0.93,'032':0.93,'043':0.93,'054':0.93,'065':0.93,u'08░':0.65,'106':1,'12undo':1.36,'14< Bks':1.46,'16° _ °':1.37,'17nwrw':0,
                      '18shift':1.4,'19-':1,'21+':1,'230':0.9,'249':0.9,'258':1,u'26░':0.65,'277':1,'28redo':1.36,'30(  )':1.23, '31Enter':1.56,'32nwrw':0,
                      '33q':1.1,'34w':1,'35e':1,'36r':1,'37t':1,'38y':1,u'39░':0.65,'40u':1,'42i':1,'43o':1,'44p':1,'45 / ':1.19,'46nwrw':0,
                      u'47。':1,'48a':1,'49s':1,'50d':1,'51f':1,'52g':1,u'53░':0.65,'57h':1,'58j':1,'59k':1,'60l':1,'61 * ':1.19,'62nwrw':0,
                      '63 % ':1,'64z':1,'65x':1,'66c':1,'67v':1,'68b':1,u'69░':0.65,'70n':1,'71m':1,u'72，':1,'73=':1,u'74 ▲ ':1.19,'75nwrw':0,
                      u'76 ◀ ':1,u"77 ▶ ":1, u'78？':1,'79.':1,   u'80':0.1,'81S P A C E':2.56,u'83':0.1,  u'84：':1, u'85！':1, u'86“ ”':1,u'88 ▼ ':1.19,'87@':1}  #2.770
        elif shift_sst==1 and lang_sst == 'CN':
            self.sym_list={'00nwrw':0,'01Lang':1.1,'021':0.93,'032':0.93,'043':0.93,'054':0.93,'065':0.93,u'08░':0.65,'106':1,'12undo':1.36,'14< Bks':1.46,'16° _ °':1.37,'17nwrw':0,
                      '18shift':1.4,u"19—":1, u'21€':1,'230':.9,'249':.9,'258':1,u'26░':0.65,'277':1,'28redo':1.36,'30[  ]':1.23,'31Enter':1.56,'32nwrw':0,
                      '33Q':1.1,'34W':1,'35E':1,'36R':1,'37T':1,'38Y':1,u'39░':0.65,'40U':1,'42I':1,'43O':1,'44P':1,'45\\':1.19,'46nwrw':0,
                      '47~':1,'48A':1,'49S':1,'50D':1,'51F':1,'52G':1,u'53░':0.65,'57H':1,'58J':1,'59K':1,'60L':1,'61< >':1.19,'62nwrw':0,
                      '63 & ':1,'64Z':1,'65X':1,'66C':1,'67V':1,'68B':1,u'69░':0.65,'70N':1,'71M':1,'72{ }':1,'73|':1,u'74 ▲ ':1.19,'75nwrw':0,
                      u'76 ◀ ':1,u'77 ▶ ':1,"78‘ ’":1,u'79 、 ':1,   u'80':0.1,'81S P A C E':2.56,u'83':0.1,  '84#':1,u'85^':1,u'86 ； ':1,u'88 ▼ ':1.19,'87 $ ':1}

        elif shift_sst==0 and lang_sst == 'EN':
            self.sym_list={'00nwrw':0,'01Lang':1.1,'021':0.93,'032':0.93,'043':0.93,'054':0.93,'065':0.93,u'08░':0.65,'106':1,'12undo':1.36,'14< Bks':1.46,'16° _ °':1.37,'17nwrw':0,
                      '18shift':1.4,'19-':1,'21+':1,'230':0.9,'249':0.9,'258':1,u'26░':0.65,'277':1,'28redo':1.36,'30(  )':1.23, '31Enter':1.56,'32nwrw':0,
                      '33q':1.1,'34w':1,'35e':1,'36r':1,'37t':1,'38y':1,u'39░':0.65,'40u':1,'42i':1,'43o':1,'44p':1,'45 / ':1.19,'46nwrw':0,
                      "47' '":1,'48a':1,'49s':1,'50d':1,'51f':1,'52g':1,u'53░':0.65,'57h':1,'58j':1,'59k':1,'60l':1,'61 * ':1.19,'62nwrw':0,
                      '63 % ':1,'64z':1,'65x':1,'66c':1,'67v':1,'68b':1,u'69░':0.65,'70n':1,'71m':1,'72,':1, '73=':1,u'74 ▲ ':1.19,'75nwrw':0,
                      u'76 ◀ ':1,u"77 ▶ ":1,'78?':1,'79.':1,   u'80':0.1,'81S P A C E':2.56,u'83':0.1,  '84:':1,'85!':1, '86" "':1,u'88 ▼ ':1.19,'87@':1}  #2.770
        elif shift_sst==1 and lang_sst == 'EN':
            self.sym_list={'00nwrw':0,'01Lang':1.1,'021':0.93,'032':0.93,'043':0.93,'054':0.93,'065':0.93,u'08░':0.65,'106':1,'12undo':1.36,'14< Bks':1.46,'16° _ °':1.37,'17nwrw':0,
                      '18shift':1.4,u"19…":1, u'21€':1,'230':.9,'249':.9,'258':1,u'26░':0.65,'277':1,'28redo':1.36,'30[  ]':1.23,'31Enter':1.56,'32nwrw':0,
                      '33Q':1.1,'34W':1,'35E':1,'36R':1,'37T':1,'38Y':1,u'39░':0.65,'40U':1,'42I':1,'43O':1,'44P':1,'45\\':1.19,'46nwrw':0,
                      '47~':1,'48A':1,'49S':1,'50D':1,'51F':1,'52G':1,u'53░':0.65,'57H':1,'58J':1,'59K':1,'60L':1,'61< >':1.19,'62nwrw':0,
                      '63 & ':1,'64Z':1,'65X':1,'66C':1,'67V':1,'68B':1,u'69░':0.65,'70N':1,'71M':1,'72{ }':1,'73|':1,u'74 ▲ ':1.19,'75nwrw':0,
                      u'76 ◀ ':1,u'77 ▶ ':1,u'78･':1,u'79 ` ':1,   u'80':0.1,'81S P A C E':2.56,u'83':0.1,  '84#':1,u'85^':1,'86 ; ':1,u'88 ▼ ':1.19,'87 $ ':1}

        elif shift_sst==0 and lang_sst == 'DE':
            self.sym_list={'00nwrw':0,'01Lang':1.1,'021':0.93,'032':0.93,'043':0.93,'054':0.93,'065':0.93,u'08░':0.65,'106':1,'12undo':1.36,'14< Bks':1.46,'16° _ °':1.37, '17nwrw':0,
                      '18shift':1.4,u'19ß':1,u"21ü":1,'230':0.9,'249':0.9,'258':1,u'26░':0.65,'277':1,'28redo':1.36,'30(  )':1.23,'31Enter':1.56, '32nwrw':0,
                      '33q':1.1,'34w':1,'35e':1,'36r':1,'37t':1,'38y':1,u'39░':0.65,'40u':1,'42i':1,'43o':1,'44p':1,u'45ä':1.19, '46nwrw':0,
                      "47' '":1,'48a':1,'49s':1,'50d':1,'51f':1,'52g':1,  u'53░':0.65,'57h':1,'58j':1,'59k':1,'60l':1,u'61ö':1.19, '62nwrw':0,
                      '63 % ':1,'64z':1,'65x':1,'66c':1,'67v':1,'68b':1,u'69░':0.65,'70n':1,'71m':1,'72,':1,'73+':1,u'74 ▲ ':1.19, '75nwrw':0,
                      u'76 ◀ ':1,u"77 ▶ ":1,'78?':1,'79.':1,   u'80':0.1,'81S P A C E':2.56,u'83':0.1,  '84:':1,'85-':1, '86" "':1,u'88 ▼ ':1.19,"87@":1} #,'88@':1
        elif shift_sst==1 and lang_sst == 'DE':
            self.sym_list={'00nwrw':0,'01Lang':1.1,'021':0.93,'032':0.93,'043':0.93,'054':0.93,'065':0.93,u'08░':0.65,'106':1,'12undo':1.36,'14< Bks':1.46,'16° _ °':1.37,'17nwrw':0,
                      '18shift':1.4,'19*':1,'21!':1,'230':0.9,'249':0.9,'258':1,u'26░':0.65, '277':1,'28redo':1.36,'30[  ]':1.23,'31Enter':1.56,'32nwrw':0,
                      '33Q':1.1,'34W':1,'35E':1,'36R':1,'37T':1,'38Y':1,u'39░':0.65,'40U':1,'42I':1,'43O':1,'44P':1,'45\\':1.19,'46nwrw':0,
                      '47=':1,'48A':1,'49S':1,'50D':1,'51F':1,'52G':1,  u'53░':0.65,'57H':1,'58J':1,'59K':1,'60L':1,'61< >':1.19,'62nwrw':0,
                      '63 & ':1,'64Z':1,'65X':1,'66C':1,'67V':1,'68B':1,u'69░':0.65,'70N':1,'71M':1,'72{ }':1,'73|':1,u'74 ▲ ':1.19,'75nwrw':0,
                      u'76 ◀ ':1,u'77 ▶ ':1,u'78^':1,u'79 ` ':1,   u'80':0.1,'81S P A C E':2.56,u'83':0.1,  "84#":1,'85 / ':1,'86 ; ':1,u'88 ▼ ':1.19,'87$':1}   #,'88$':1
        #---
        if self.parent.frm_pop_scrl.winfo_viewable()== 1:
            if '30(  )' in self.sym_list:   self.sym_list['30* * *'] = self.sym_list.pop('30(  )')
            if '30[  ]' in self.sym_list:   self.sym_list['30* * *'] = self.sym_list.pop('30[  ]')
            if '31Enter' in self.sym_list:   self.sym_list['31<<<='] = self.sym_list.pop('31Enter')
            #

    def setup_kbd(self):        #
        del self.lzt_butn_lst[:]
        del self.butn_stndr_color[:]
        dark_butn_lst = ('f','j','F','J','(  )','[  ]','° _ °','shift')
        repeat_lst = ('< Bks', u' ▲ ', u' ◀ ', u' ▶ ', u' ▼ ')
        for k, v in sorted(self.sym_list.iteritems()):
            if k[2:] == 'nwrw' :
                crnt_row = tk.Frame(self , relief='flat' , borderwidth=0, bg='white')                           #
                crnt_row.pack(fill='both', expand=1, side='top', pady = 1, ipady=1, padx = 0, ipadx=0 )         #
                continue
            elif k[2:] == u'░' :  crnt_butn = tk.Button(crnt_row, text=k[2:], font=('Sans','8','bold'), relief='solid', borde =1, bd=1,overrelief='solid', activebackground='grey95', activeforeground='grey10', bg='grey95', fg='grey10',
                                          padx=-1, width=int(v*5.41), height=int(self.keysize*0.1), state='disabled', command=lambda x=k[2:]: self.kbd_key_pressed(x) )  #3.96
            elif k[2:] == '' :  crnt_butn = tk.Button(crnt_row, text=k[2:], font=('Sans','8','bold'), relief='flat', borde =1, bd=1,overrelief='flat', activebackground='grey42', activeforeground='grey10', bg='grey42', fg='grey10',   #50
                                          padx=-1, width=int(v*5.41), height=int(self.keysize*0.1), state='disabled', command=lambda x=k[2:]: self.kbd_key_pressed(x) )
            elif k[2:] in dark_butn_lst :  crnt_butn = tk.Button(crnt_row, text=k[2:], font=('Sans','8','bold'), relief='solid', borde =1, bd=1,overrelief='solid', activebackground='grey85', activeforeground='grey10', bg='grey86', fg='grey10',
                                          padx=-1, width=int(v*5.41), height=int(self.keysize*0.1), command=lambda x=k[2:]: self.kbd_key_pressed(x) )  #5.96
            elif k[2:] in repeat_lst :  crnt_butn = tk.Button(crnt_row, text=k[2:], font=('Sans','8','bold'), relief='solid', borde =1, bd=1,overrelief='solid', activebackground='grey100', activeforeground='grey10', bg='white', fg='grey10',
                                          padx=-1, width=int(v*5.41), height=int(self.keysize*0.1), repeatdelay=256, repeatinterval=256, command=lambda x=k[2:]: self.kbd_key_pressed(x) )  #5.96
            else :  crnt_butn = tk.Button(crnt_row, text=k[2:], font=('Sans','8','bold'), relief='solid', borde =1, bd=1,overrelief='solid', activebackground='grey100', activeforeground='grey10', bg='white', fg='grey10',
                                          padx=-1, width=int(v*5.41), height=int(self.keysize*0.1), command=lambda x=k[2:]: self.kbd_key_pressed(x) )  #5.96
            crnt_butn.pack(fill='y', expand=1, side='left')  #5.96 # print int(v*5.41), k
            self.lzt_butn_lst.append(crnt_butn)
            self.butn_stndr_color.append((crnt_butn['bg'],crnt_butn['fg'],crnt_butn['activebackground'],crnt_butn['activeforeground'],crnt_butn['state']))

    def updata_kbd(self, shift_sst, lang_sst):
        self.shift_state=shift_sst
        self.lang_state=lang_sst
        self.mapping_kbd_symb(shift_sst, lang_sst)        # sym_lst = sorted(self.sym_list)
        sym_lst_clen=[]
        for k, v in sorted(self.sym_list.iteritems()):
            if k[2:] != 'nwrw' :  sym_lst_clen.append((k[2:],v))
        for sym, butn, clor in zip(sym_lst_clen, self.lzt_butn_lst, self.butn_stndr_color):        #
            butn.config(state=clor[4], text=sym[0], width=int(sym[1]*5.41), bg=clor[0],fg=clor[1], activebackground=clor[2], activeforeground=clor[3], command=lambda bb=sym[0]: self.kbd_key_pressed(bb) )  #5.96
        for rd_btn in self.parent.radio_butn_lst: rd_btn.config(bg='grey80', fg='grey0', state='normal')
        #
        if self.parent.paint and self.parent.paint.winfo_exists():
            if self.parent.paint.winfo_ismapped():  #pnt_root
                for btn in self.lzt_butn_lst:btn.config(state='disable')  #bg='grey85', fg='grey70',
                for rd_btn in self.parent.radio_butn_lst: rd_btn.config(state='disable')  #bg='grey85', fg='grey70',
                return
        if self.parent.frm_pop_scrl.winfo_viewable()==1:
            for btn in self.lzt_butn_lst:
                btn.config(bg='grey85', fg='grey70', state='disable')
                if btn['text'] in ('< Bks', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9') :btn.config(bg='grey32', fg='grey100', activebackground='grey32', activeforeground='grey100', state='normal')
                if btn['text'] in ('* * *', '<<<=', 'undo', 'redo', u' ▲ ', u' ◀ ', u' ▶ ', u' ▼ ') : btn.config(bg='grey100', fg='grey10', activebackground='grey100', activeforeground='grey10', state='normal')
            for rd_btn in self.parent.radio_butn_lst: rd_btn.config(bg='grey85', fg='grey70', state='disable')

    def kbd_key_pressed(self, k):
        if k not in self.fctn_key_dic.keys():    self.ipt_widget.insert(tk.INSERT, k.strip())
        else :  self.fctn_key_dic[k](k)                 #self.fctn_key_dic[k.encode('utf-8')](k)
        if self.ipt_widget == self.parent.tx_ipt_pinyin :
            self.parent.main_tx.focus_force()
            self.parent.main_tx.see(self.parent.main_tx.index(tk.INSERT))    ## self.ipt_widget.tk_focusFollowsMouse()

    def destroy_kbd(self):   self.destroy()             # for wdg in self.children.values() : wdg.destroy()

class TK_PAINT(tk.Frame):
    __slots__ = ('active_button', 'butn_quit', 'choose_color_sldr', 'choose_size_sldr', 'cnvs_main', 'color', 'color_vlu', 'color_vlu_shw', 'eraser_butn', 'eraser_on', 'first_pnt', 'info_label', 'line_width', 'lst_bx_open', 'main_h', 'old_x', 'old_y', 'open_img_butn', 'pen_butn', 'pic_pth', 'pnt_root', 'prj_pth_txt_odn', 'save_img_butn', 'scrlbar_open_lst', 'size_vlu', 'size_vlu_shw', 'ypos_opbx', 'parent', 'ui_lang_p')
    def __init__(self, parent):
        tk.Frame.__init__(self, takefocus=0)
        self.parent = parent
        self.pnt_root = tk.Frame(self, relief='flat', borderwidth=0, bg='grey100', highlightbackground='grey100', highlightthickness=0)
        self.pnt_root.pack(fill='both', expand=1, side='top', pady = 7, padx = 0 )

        self.prj_pth_txt_odn = ''.join((os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), '/txbook/'))
        if not os.path.isdir(self.prj_pth_txt_odn): os.mkdir(self.prj_pth_txt_odn)

        self.color_vlu, self.size_vlu = tk.IntVar(), tk.IntVar()
        self.color_vlu_shw, self.size_vlu_shw = tk.StringVar(), tk.StringVar()
        butn_w, butn_h = 2, 2

        self.ui_lang_p='en'
        self.color = 'black'
        self.line_width, self.eraser_on = 2, 0
        self.pic_pth = None
        self.old_x, self.old_y = None, None
        self.ypos_opbx, self.main_h = 2, 950+60

        self.pen_butn = tk.Button(self.pnt_root, font=('Sans','6','bold'), activebackground='grey100', activeforeground='black', bg='grey100', fg='black', relief='solid', borderwidth=2, text='PenciL', height = butn_h, width = butn_w, command=self.use_pen)
        self.pen_butn.grid(row=1, column=0, sticky= 'w')#, ipadx=3

        self.eraser_butn = tk.Button(self.pnt_root,font=('Sans','6','bold'), activebackground='grey100', activeforeground='black', bg='grey100', fg='black', relief='solid', borderwidth=2, text='Eraser', height = butn_h, width = butn_w, command=self.use_eraser)
        self.eraser_butn.grid(row=1, column=1)
        #-----
        frm_lab_size = tk.Frame(self.pnt_root, bg='white', relief='flat', borderwidth=0 )   #∙」「•」「・」「●」
        frm_lab_size.grid(row=1, column=2, sticky= 'ne', ipadx=60, ipady=0)

        self.choose_size_sldr = tk.Scale(frm_lab_size, width = 60, sliderlength=70, variable=self.size_vlu, from_=32, to=1, bd=0, borderwidth=1, relief='solid', bg='grey80', showvalue=0, sliderrelief='raised', orient='horizontal', activebackground='grey80', highlightbackground='black',troughcolor='white', highlightthickness=1, command = self.choose_size)
        self.choose_size_sldr.set(2)
        self.choose_size_sldr.pack(fill='x', expand=1, side='bottom', anchor= 'ne')    #.grid(row=1, column=2, sticky= 'e')

        size_label_c = tk.Label(frm_lab_size, font=('Sans','5','bold'), width=10, bg='grey100', textvariable=self.size_vlu_shw, anchor= 'e')    #
        size_label_c.pack(fill='x',expand=0, side='top',anchor= 'ne', ipadx=2)    #
        #---------------------------------
        self.butn_quit=tk.Checkbutton(self.pnt_root, height = 1, width = 5, font=('Sans','7','bold'), text='quit', anchor='w', activebackground='grey60', bg='grey60', fg='black',borderwidth=1, underline=-1, highlightbackground='black', highlightcolor='black', highlightthickness=1,offrelief='flat', overrelief='raise', relief='solid', bd=1, command = self.quit_paint)  #selectcolor='red',
        self.butn_quit.grid(row=1, column=3, pady=4, sticky= 'n')

        self.info_label = tk.Label(self.pnt_root,font=('Sans','4','normal'), state='normal', height = 2, width = 20, anchor='center', fg='grey20', bg='grey100', relief='solid', borderwidth=0, highlightbackground='grey50', text=u'click " quit > cancel "\nto reset canvas' )  #compound='left',
        self.info_label.grid(row=1, column=3, sticky= 's')
        #---------------------------------
        frm_lab_color = tk.Frame(self.pnt_root, bg='white', relief='flat', borderwidth=0 )
        frm_lab_color.grid(row=1, column=4, sticky= 'nw', ipadx=60, ipady=0)

        self.choose_color_sldr = tk.Scale(frm_lab_color, width = 60, sliderlength=70, variable=self.color_vlu, from_=1, to=16, bd=0, borderwidth=1, relief='solid', bg='grey60', showvalue=0, sliderrelief='raised', orient='horizontal', activebackground='grey60', highlightbackground='black',troughcolor='white', highlightthickness=1, command=self.choose_color)
        self.choose_color_sldr.pack(fill='x',expand=1, side='bottom', anchor= 'nw') #

        color_label_s = tk.Label(frm_lab_color, font=('Sans','5','bold'), width=10, bg='grey100', textvariable= self.color_vlu_shw, anchor= 'w')   #compound='right'
        color_label_s.pack(fill='x',expand=0, side='top', anchor= 'nw',ipadx=2) #
        #---
        self.open_img_butn = tk.Button(self.pnt_root,font=('Sans','6','bold'), activebackground='grey100', activeforeground='black', bg='grey100', fg='black', relief='solid', borderwidth=2, text='Open', height = butn_h, width = butn_w, command=self.butn_open_clicked)
        self.open_img_butn.grid(row=1, column=5)

        self.save_img_butn = tk.Button(self.pnt_root,font=('Sans','6','bold'), activebackground='grey100', activeforeground='black', bg='grey100', fg='black', relief='solid', borderwidth=2, text='Save', height = butn_h, width = butn_w, command=self.save_bitmap)
        self.save_img_butn.grid(row=1, column=6, sticky= 'e', pady = 3)#
        #---
        self.cnvs_main = tk.Canvas(self.pnt_root, bg='white', width=1245, height=self.main_h, borderwidth=1, highlightthickness=1, highlightbackground='black')
        self.cnvs_main.grid(row=0, columnspan=7)

        self.cnvs_main.bind('<B1-Motion>', self.paint)
        self.cnvs_main.bind('<ButtonRelease-1>', self.reset)        #

        self.lst_bx_open = tk.Listbox(self.pnt_root, font=("Sans", 5, 'normal'), relief='solid', borderwidth=0, highlightcolor='white',highlightbackground='white', activestyle='none',selectborderwidth=23, selectforeground='black', selectbackground='white', highlightthickness=0, bg ='grey80', selectmode = 'SINGLE')
        self.lst_bx_open.grid(row=0, column=0, sticky='e')
        self.lst_bx_open.place_configure(x = 1280, y = self.ypos_opbx, width = 0, height = self.main_h)  #1249
        self.lst_bx_open.bind("<<ListboxSelect>>", self.open_lst_item_clicked)

        self.scrlbar_open_lst = tk.Scrollbar( self.pnt_root , orient='vertical', activebackground='grey50', relief='solid',borderwidth=0, bg='grey70', elementborderwidth=1, highlightbackground='white',troughcolor='white', command=self.lst_bx_open.yview )
        self.scrlbar_open_lst.place(x = 1280, y = self.ypos_opbx, height=self.main_h, width =0)
        self.lst_bx_open['yscrollcommand'] = self.scrlbar_open_lst.set

        self.active_button = self.pen_butn
        self.pen_butn.config(relief='sunken')

    def use_pen(self):
        if self.choose_color_sldr.get()>1 :
            self.choose_color_sldr.set(self.choose_color_sldr.get()-1)
            self.choose_color_sldr.set(self.choose_color_sldr.get()+1)
        else :
            self.choose_color_sldr.set(self.choose_color_sldr.get()+1)
            self.choose_color_sldr.set(self.choose_color_sldr.get()-1)
        self.activate_button(self.pen_butn)

    def use_eraser(self):
        if self.choose_color_sldr.get()>1 :
            self.choose_color_sldr.set(self.choose_color_sldr.get()-1)
            self.choose_color_sldr.set(self.choose_color_sldr.get()+1)
        else :
            self.choose_color_sldr.set(self.choose_color_sldr.get()+1)
            self.choose_color_sldr.set(self.choose_color_sldr.get()-1)
        self.activate_button(self.eraser_butn, eraser_mode=1)
        self.pnt_root.after(10, lambda: self.info_label.config( text = 'click " PenciL" button\n to draw image' ) )  #

    def choose_color(self, value): #self.eraser_on = 0
        self.color_vlu_shw.set( "brush color index : {}".format(self.color_vlu.get()) )
        color_vlu_map = ''.join(('grey', str( abs(int(100/16.0) * (int(value)-1)) )))
        self.color = 'white' if self.eraser_on else color_vlu_map
        self.choose_color_sldr.config( bg= color_vlu_map, activebackground=color_vlu_map )        #

    def choose_size(self, value):
        self.size_vlu_shw.set( u"{} : o ● • size brush".format(self.size_vlu.get()) )
        self.line_width = value

    def activate_button(self, some_button, eraser_mode=0):
        self.active_button.config(relief='raised')
        some_button.config(relief='sunken')
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):        # round butt projecting  #BEVEL  MITER  ROUND
        if self.old_x and self.old_y:            #
            self.cnvs_main.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill=self.color, capstyle='round', joinstyle = 'round', smooth=1, splinesteps=32)
        self.old_x, self.old_y = event.x, event.y

    def show_first_pnt(self, event):        #for brush offset
        try: self.cnvs_main.unbind('<B1-Motion>')
        except: pass                #
        self.first_pnt = self.cnvs_main.create_rectangle( event.x-(int(self.line_width)/2 +2 ), event.y-(int(self.line_width)/2 + 2)-84,event.x+(int(self.line_width)/2 + 2 ), event.y+(int(self.line_width)/2 +2 )-84 )
        self.old_x, self.old_y = event.x, event.y
        self.pnt_root.after(320, lambda : self.cnvs_main.bind('<B1-Motion>', self.paint) )

    def reset(self, event):
        self.old_x, self.old_y = None, None
        try : self.cnvs_main.delete(self.first_pnt)        #
        except : pass                   #

    def save_bitmap(self):
        os.popen("screenshot")          #
        self.save_img_butn.config(state='disable')
        self.pnt_root.after(500, self.mov_lastest_file)

    def cnvrt_png_gif(self, ipt_pth):
        ssht_file_lst = [ ipt_pth + x for x in os.listdir(ipt_pth) if os.path.isfile(ipt_pth + x) and x.lower().endswith('.png') ]
        if not ssht_file_lst : return        #
        latest_ssht = max(ssht_file_lst, key=os.path.getctime)
        #
        imk_cnvrt_pth = ''.join((os.path.dirname(os.path.abspath(__file__)), '/convert -crop 1245x1011+8+8 -resize 1245x1011 +profile "*" '))
        os.popen( ''.join((imk_cnvrt_pth, latest_ssht, ' ', latest_ssht[:-4], '.gif')) )        # print imk_cnvrt_pth

    def mov_lastest_file(self):
        self.save_img_butn.config(state='normal')
        ipt_pth = '/mnt/us/'
        self.cnvrt_png_gif(ipt_pth)
        #---
        ssht_file_lst = [ ipt_pth + x for x in os.listdir(ipt_pth) if os.path.isfile(ipt_pth + x) and x.endswith('.gif') ]
        if not ssht_file_lst : return
        latest_ssht = max(ssht_file_lst, key=os.path.getctime)
        if not os.path.isfile( ''.join((self.prj_pth_txt_odn, os.path.basename(latest_ssht))) ):
            os.popen( ''.join(('mv ', latest_ssht, ' ', self.prj_pth_txt_odn, os.path.basename(latest_ssht)[13:-9].replace('_', ''),'.gif')) )#
        else :   #
            quit_id = self.after( 420000, lambda : self.destroy() )            #
            rslt = tkmsgbx_ask_yes_no('L:D_N:dialog_ID:PySide7','The file is exists,\nDo you want overwrite it ?\n\n文件已存在, 是否覆盖 ?',icon='info')
            if rslt :
                self.after_cancel(quit_id)          #
                os.popen( ''.join(('mv ', latest_ssht, ' ', self.prj_pth_txt_odn, os.path.basename(latest_ssht)[13:-9].replace('_', ''), '.gif')) )
            else : self.after_cancel(quit_id)       #
        self.info_label['text'] = ''.join(('file is saved :\n', os.path.basename(latest_ssht)[13:-9].replace('_', ''), '.gif'))
        #---
        if not os.path.isdir( ''.join((ipt_pth, 'screenshot_bak')) ): os.mkdir( ''.join((ipt_pth, 'screenshot_bak') ))
        os.popen( ''.join(('mv ', latest_ssht[:-4], '.png', ' ', ipt_pth, 'screenshot_bak/')) )

    def quit_paint(self):
        open_lst_sze = tuple([int(x) for x in self.lst_bx_open.winfo_geometry().split('+')[0].split('x')])
        if  open_lst_sze[0] > 1 : self.butn_open_clicked()
        #---
        for child in self.pnt_root.winfo_children():        #freeze other widget
            if not isinstance(child, tk.Frame) and not isinstance(child, tk.Scrollbar): child.configure(state='disable')
        self.info_label['text'] = (u'click " quit > cancel "\nto reset canvas')        #
        quit_id = self.after( 61800, lambda : [self.destroy(), self.parent.updated_keyboard_state()] )     #
        rslt = tkmsgbx_ask_yes_no('Do you want to quit N31_PainT ?\n是否退出 N31_PainT ? 点击 "cancel" 重置画板 .\n\nClick "cancel" button to reset canvas .\nN31_PainT close in 1 minute if no response !',icon='info', parent = self.pnt_root)    #self.pnt_root
        #---
        if rslt :
            self.destroy()
            self.parent.updated_keyboard_state()
        else :      # self.butn_quit.flash()
            self.after_cancel(quit_id)                      #
            try :
                for child in self.pnt_root.winfo_children():        #unfreeze other widget
                    if not isinstance(child, tk.Frame) and not isinstance(child, tk.Scrollbar): child.configure(state='normal')
            except: pass
            try:
                self.butn_quit.deselect()
                if rslt is None: self.cnvs_main.delete("all")
            except: pass

    def butn_open_clicked(self) :
        open_lst_sze = tuple([int(x) for x in self.lst_bx_open.winfo_geometry().split('+')[0].split('x')])
        if  open_lst_sze[0] > 1 :
            self.lst_bx_open.place_configure(x = 1249, y = self.ypos_opbx, width = 0, height = self.main_h)
            self.scrlbar_open_lst.place_configure(x = 1249, y = self.ypos_opbx, width =0, height=self.main_h)
            self.open_img_butn['text'] = 'Open'
            self.save_img_butn['state'] = 'normal'
            self.info_label['text'] = ('right sidebar is closed')
        else :
            self.lst_bx_open.place_configure(x = 900, y = self.ypos_opbx, width = 349, height = self.main_h)
            self.scrlbar_open_lst.place_configure(x = 1249-72, y = self.ypos_opbx, width =72, height=self.main_h)
            self.open_img_butn['text'] = '↹ Slide'
            self.save_img_butn['state'] = 'disable'
            self.info_label['text'] = (u'click " ↹ Slide" button\nto close right sidebar')
        self.fill_open_files_list()

    def fill_open_files_list(self):
        self.lst_bx_open.delete(0,tk.END)
        img_fmt_lst = ('.gif', '.png', '.jpg', '.xpm', '.pgm', '.ppm')
        for ff in os.listdir(self.prj_pth_txt_odn):
            if os.path.isfile( ''.join((self.prj_pth_txt_odn, ff)) ) and ff[-4:].lower() in img_fmt_lst:
                self.lst_bx_open.insert(tk.END, ff.decode('utf-8'))
        self.lst_bx_open.insert(tk.END, u'[- Ui_lang:界面语 -]')
        self.lst_bx_open.insert(tk.END, u'[- Open ExploreR -]')

    def open_lst_item_clicked(self, event=None):
        crnt_shnm = self.lst_bx_open.get(self.lst_bx_open.curselection())
        crnt_idx = self.lst_bx_open.index('anchor')
        if crnt_shnm == u'[- Open ExploreR -]' and crnt_idx == self.lst_bx_open.size() -1:
            os.popen("exec /mnt/us/extensions/explorer/bin/explorer.sh")            #
            self.info_label['text'] = ( 'explorer is opened !' )
            return
        if crnt_shnm == u'[- Ui_lang:界面语 -]' and crnt_idx == self.lst_bx_open.size() -2:
            self.ui_lang_switch()
            #
            return
        #---
        if not crnt_shnm or not os.path.isfile( ''.join((self.prj_pth_txt_odn, crnt_shnm)) ): return
        if os.path.getsize( ''.join((self.prj_pth_txt_odn, crnt_shnm)) )>9788000: #32768000: 32Mb   #10240000: 10Mb
            self.info_label['text'] = ''.join(('file is bigger than 9.5 mb,\nskip : ', crnt_shnm))
            return
        #---
        if crnt_shnm[-4:].lower() in ('.gif', '.pgm', '.ppm'):
            self.open_bitmap_action( ''.join((self.prj_pth_txt_odn, crnt_shnm)) )
        else :
            cvted_pth = self.img_fmt_cvt(crnt_shnm)
            self.open_bitmap_action(cvted_pth)
        self.info_label['text'] = ''.join(('file is opened :\n', crnt_shnm))

    def open_bitmap_action(self, img_pth):
        self.cnvs_main.delete("all")        #
        self.pic_pth = tk.PhotoImage(file=img_pth)    #tk.PhotoImage(file="c:/temp/xxx.gif")
        img_ofst_x, img_ofst_y = int(self.cnvs_main.winfo_rootx())*-1, int(self.cnvs_main.winfo_rooty())*-1
        if int(self.pic_pth.width())<=int(self.cnvs_main.cget('width')) and int(self.pic_pth.height()) <= int(self.cnvs_main.cget('height')):
            img_ofst_x, img_ofst_y = 0, 0
        # ---
        self.cnvs_main.create_image(img_ofst_x, img_ofst_y, image=self.pic_pth, anchor='nw')        #

    def img_fmt_cvt(self, org_shnm):
        if not os.path.isdir( ''.join((self.prj_pth_txt_odn, 'img_cvt_tmp')) ): os.mkdir( ''.join((self.prj_pth_txt_odn, 'img_cvt_tmp')) )
        os.popen( ''.join(('cp ', self.prj_pth_txt_odn, org_shnm, ' ', self.prj_pth_txt_odn, 'img_cvt_tmp')) )
        org_img_lng_nm = ''.join((self.prj_pth_txt_odn, 'img_cvt_tmp/', org_shnm))
        cvted_img_lng_nm = ''.join((self.prj_pth_txt_odn, 'img_cvt_tmp/',  org_shnm[:-4], '.gif'))
        os.popen( ''.join((os.path.dirname(os.path.abspath(__file__)), '/convert ', org_img_lng_nm, ' ', cvted_img_lng_nm)) )
        if os.path.isfile(org_img_lng_nm) : os.popen( ''.join(('rm ', org_img_lng_nm)) )
        self.pnt_root.after( 32000, lambda: os.popen( ''.join(('rm ', cvted_img_lng_nm)) ) )
        return cvted_img_lng_nm

    def ui_lang_switch(self):
        butn_tx_dic_p = {u'↹ Slide':u'↹ 滑隱', u'PenciL':u'铅笔', u'Eraser':u'橡皮', u'Open':u'打开', u'Save':u'保存', u'quit':u'退出', u'click " quit > cancel "\nto reset canvas':u'点击"退出" > "cancel"\n重置画板', u'click " PenciL" button\n to draw image':u'点击"铅笔"按钮\n继续涂画'}
        main_wdg_p = self.pnt_root.winfo_children()
        for sub_wdg_p in main_wdg_p :
            if sub_wdg_p.winfo_children():    main_wdg_p.extend(sub_wdg_p.winfo_children())
        for ii_p in list(set(main_wdg_p)):
            tt_p = ii_p.winfo_class()
            if tt_p in ('Text', 'Button',  'Radiobutton', 'Checkbutton', 'Label', 'Listbox'):  #
                try :
                    if self.ui_lang_p == 'en' :           #en_ui_to_cn
                        if ii_p['text'] in butn_tx_dic_p.keys():
                            ii_p['text'] = butn_tx_dic_p[ii_p['text']]
                    else :
                        if ii_p['text'] in butn_tx_dic_p.values():
                            ii_p['text'] = butn_tx_dic_p.keys()[butn_tx_dic_p.values().index(ii_p['text'])]
                except : pass
        self.ui_lang_p = 'cn' if self.ui_lang_p == 'en' else 'en'

def run_kte(): N31_KTE_TKN()


if __name__ == '__main__':
    run_kte()
# todolist hardware button, dict:en cn de,  update novel