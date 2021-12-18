
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

    # background_color = (245, 245, 245)
    # foreground_color = (30, 30, 30)
    # foreground_color2 = (50, 50, 50)

    background_color = (30, 30, 30)
    foreground_color = (255, 255, 255)
    foreground_color2 = (205, 205, 205)

    self_button2 = '''QPushButton{background-color: rgb(245,135,45);
        height: 35px;
        border-style: outset;
        border-width: 0px;
        border-radius: 4px;
        border-color: rgb(90,90,90);
        font: bold 17px "Microsoft JhengHei UI";
        color: rgb(%d,%d,%d);}
        QPushButton:hover{background-color: rgb(245,105,35);
        }
        QPushButton:pressed{background-color: rgb(245,65,25);
        }
        QPushButton:disabled{background-color: rgb(100,100,100);
        }''' % foreground_color2
