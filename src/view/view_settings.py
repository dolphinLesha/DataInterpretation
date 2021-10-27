
class ViewSettings:
    control_width: int = 250

    tab_button_design_no_taped: str = '''QPushButton{background-color: rgb(255,255,255);
            border-style: outset;
            border-bottom-width: 4px;
            border-top-left-radius: 2px;
            border-top-right-radius: 2px;
            border-color: rgb(150,150,150);
            font: bold 14px "Microsoft JhengHei UI";
            color: rgb(60,60,60);}
            QPushButton:hover{background-color: rgb(200,255,255);}
            QPushButton:pressed{background-color: rgb(170,255,255);
            }'''
    tab_button_design_taped: str = '''QPushButton{background-color: rgb(210,210,210);
            border-style: outset;
            border-width: 0px;
            border-top-left-radius: 2px;
            border-top-right-radius: 2px;
            border-color: rgb(150,150,150);
            font: 14px "Microsoft JhengHei UI";
            color: rgb(60,60,60);}
            QPushButton:hover{background-color: rgb(200,200,200);
            border-bottom-width: 4px;}
            QPushButton:pressed{background-color: rgb(190,190,190);
            }'''