
NAME = "港铁资源包"
UUID = "8f0dea66-0776-4992-9f71-7408aad8bb2f"
ALL_LINE_LIST = ['TWL', 'ISL', 'KTL', 'TML', 'TKL', 'TKZ', 'ERL', 'ERZ', 'DCL', 'SIL', 'DRL', 'AEL']
ALL_LINE_DICT = {'荃湾线': 'TWL', '港岛线': 'ISL', '观塘线': 'KTL', '屯马线': 'TML', '将军澳线（主线）': 'TKL', '将军澳线（支线）': 'TKZ', '东铁线（主线）': 'ERL', '东铁线（支线）': 'ERZ', '东涌线': 'DCL', '南港岛线': 'SIL', '迪士尼线': 'DRL', '机场快线': 'AEL'}
ABOVE_ZERO_DIRECTION = {'TWL': '开往 荃湾 方向', 'ISL': '开往 坚尼地城 方向', 'KTL': '开往 调景岭 方向', 'TML': '开往 屯门 方向', 'TKL': '开往 北角 方向', 'TKZ': '开往 北角 方向', 'ERL': '开往 金钟 方向', 'ERZ': '开往 金钟 方向', 'DCL': '开往 东涌 方向', 'SIL': '开往 海怡半岛 方向', 'DRL': '开往 欣澳 方向', 'AEL': '开往 博览馆 方向'}
BELOW_ZERO_DIRECTION = {'TWL': '开往 中环 方向', 'ISL': '开往 柴湾 方向', 'KTL': '开往 黄埔 方向', 'TML': '开往 乌溪沙 方向', 'TKL': '开往 宝琳 方向', 'TKZ': '开往 康城 方向', 'ERL': '开往 罗湖 方向', 'ERZ': '开往 落马洲 方向', 'DCL': '开往 香港 方向', 'SIL': '开往 金钟 方向', 'DRL': '开往 迪士尼 方向', 'AEL': '开往 香港 方向'}
TIME_DICT = {'TWL': '首班车  06:00\n末班车  01:22', 'ISL': '首班车  05:55\n末班车  00:35', 'KTL': '首班车  06:07\n末班车  01:08', 'TML': '首班车  05:38\n末班车  01:22', 'TKL': '首班车  05:57\n末班车  01:26', 'TKZ': '首班车  05:57\n末班车  01:26', 'ERL': '首班车  05:28\n末班车  01:09', 'ERZ': '首班车  05:28\n末班车  01:09', 'DCL': '首班车  05:59\n末班车  01:09', 'SIL': '首班车  06:00\n末班车  01:14', 'DRL': '首班车  06:15\n末班车  00:45', 'AEL': '首班车  05:50\n末班车  01:13'}
RGB_DICT = {'TWL': 'rgb(226,35,26)', 'ISL': 'rgb(0,113,206)', 'KTL': 'rgb(0,175,65)', 'TML': 'rgb(154,56,32)', 'TKL': 'rgb(163,94,181)', 'TKZ': 'rgb(163,94,181)', 'ERL': 'rgb(97,180,228)', 'ERZ': 'rgb(97,180,228)', 'DCL': 'rgb(243,139,0)', 'SIL': 'rgb(182,189,0)', 'DRL': 'rgb(231,119,203)', 'AEL': 'rgb(0,112,120)'}
BRANCH_LINE_LIST = [['TKL', 'TKZ'], ['ERL', 'ERZ']]
DIRECT_LINE_LIST = [['None', '开往 None 方向']]
            
class Line_TWL:
                
    TsuenWan = ['TWL', 1]
                    
    TaiWoHau = ['TWL', 2]
                    
    KwaiHing = ['TWL', 3]
                    
    KwaiFong = ['TWL', 4]
                    
    LaiKing = ['TWL', 5]
                    
    MeiFoo = ['TWL', 6]
                    
    LaiChiKok = ['TWL', 7]
                    
    CheungShaWan = ['TWL', 8]
                    
    ShamShuiPo = ['TWL', 9]
                    
    PrinceEdward = ['TWL', 10]
                    
    MongKok = ['TWL', 11]
                    
    YauMaTei = ['TWL', 12]
                    
    Jordan = ['TWL', 13]
                    
    TsimShaTsui_EastTsimShaTsui = ['TWL', 14]
                    
    Admiralty = ['TWL', 15]
                    
    Central_HongKong = ['TWL', 16]
                    
class Line_ISL:
                
    KennedyTown = ['ISL', 1]
                    
    HKU = ['ISL', 2]
                    
    SaiYingPun = ['ISL', 3]
                    
    SheungWan = ['ISL', 4]
                    
    Central_HongKong = ['ISL', 5]
                    
    Admiralty = ['ISL', 6]
                    
    WanChai = ['ISL', 7]
                    
    CausewayBay = ['ISL', 8]
                    
    TinHau = ['ISL', 9]
                    
    FortressHill = ['ISL', 10]
                    
    NorthPoint = ['ISL', 11]
                    
    QuarryBay = ['ISL', 12]
                    
    TaiKoo = ['ISL', 13]
                    
    SaiWanHo = ['ISL', 14]
                    
    ShauKeiWan = ['ISL', 15]
                    
    HengFaChuen = ['ISL', 16]
                    
    ChaiWan = ['ISL', 17]
                    
class Line_KTL:
                
    TiuKengLeng = ['KTL', 1]
                    
    YauTong = ['KTL', 2]
                    
    LamTin = ['KTL', 3]
                    
    KwunTong = ['KTL', 4]
                    
    NgauTauKok = ['KTL', 5]
                    
    KowloonBay = ['KTL', 6]
                    
    ChoiHung = ['KTL', 7]
                    
    DiamondHill = ['KTL', 8]
                    
    WongTaiSin = ['KTL', 9]
                    
    LokFu = ['KTL', 10]
                    
    KowloonTong = ['KTL', 11]
                    
    ShekKipMei = ['KTL', 12]
                    
    PrinceEdward = ['KTL', 13]
                    
    MongKok = ['KTL', 14]
                    
    YauMaTei = ['KTL', 15]
                    
    HoManTin = ['KTL', 16]
                    
    Whampoa = ['KTL', 17]
                    
class Line_TML:
                
    TuenMun = ['TML', 1]
                    
    SiuHong = ['TML', 2]
                    
    TinShuiWai = ['TML', 3]
                    
    LongPing = ['TML', 4]
                    
    YuenLong = ['TML', 5]
                    
    KamSheungRoad = ['TML', 6]
                    
    TsuenWanWest = ['TML', 7]
                    
    MeiFoo = ['TML', 8]
                    
    NamCheong = ['TML', 9]
                    
    Austin = ['TML', 10]
                    
    TsimShaTsui_EastTsimShaTsui = ['TML', 11]
                    
    HungHom = ['TML', 12]
                    
    HoManTin = ['TML', 13]
                    
    ToKwaWan = ['TML', 14]
                    
    SungWongToi = ['TML', 15]
                    
    KaiTak = ['TML', 16]
                    
    DiamondHill = ['TML', 17]
                    
    HinKeng = ['TML', 18]
                    
    TaiWai = ['TML', 19]
                    
    CheKungTemple = ['TML', 20]
                    
    ShaTinWai = ['TML', 21]
                    
    CityOne = ['TML', 22]
                    
    ShekMun = ['TML', 23]
                    
    TaiShuiHang = ['TML', 24]
                    
    HengOn = ['TML', 25]
                    
    MaOnShan = ['TML', 26]
                    
    WuKaiSha = ['TML', 27]
                    
class Line_TKL:
                
    NorthPoint = ['TKL', 1]
                    
    QuarryBay = ['TKL', 2]
                    
    YauTong = ['TKL', 3]
                    
    TiuKengLeng = ['TKL', 4]
                    
    TseungKwanO = ['TKL', 5]
                    
    HangHau = ['TKL', 6]
                    
    PoLam = ['TKL', 7]
                    
class Line_TKZ:
                
    NorthPoint = ['TKZ', 1]
                    
    QuarryBay = ['TKZ', 2]
                    
    YauTong = ['TKZ', 3]
                    
    TiuKengLeng = ['TKZ', 4]
                    
    TseungKwanO = ['TKZ', 5]
                    
    LOHAS1o1Park = ['TKZ', 6]
                    
class Line_ERL:
                
    Admiralty = ['ERL', 1]
                    
    ExhibitionCentre = ['ERL', 2]
                    
    HungHom = ['ERL', 3]
                    
    MongKokEast = ['ERL', 4]
                    
    KowloonTong = ['ERL', 5]
                    
    TaiWai = ['ERL', 6]
                    
    ShaTin = ['ERL', 7]
                    
    FoTan = ['ERL', 8]
                    
    University = ['ERL', 9]
                    
    TaiPoMarket = ['ERL', 10]
                    
    TaiWo = ['ERL', 11]
                    
    Fanling = ['ERL', 12]
                    
    SheungShui = ['ERL', 13]
                    
    LoWu = ['ERL', 14]
                    
class Line_ERZ:
                
    Admiralty = ['ERZ', 1]
                    
    ExhibitionCentre = ['ERZ', 2]
                    
    HungHom = ['ERZ', 3]
                    
    MongKokEast = ['ERZ', 4]
                    
    KowloonTong = ['ERZ', 5]
                    
    TaiWai = ['ERZ', 6]
                    
    ShaTin = ['ERZ', 7]
                    
    FoTan = ['ERZ', 8]
                    
    University = ['ERZ', 9]
                    
    TaiPoMarket = ['ERZ', 10]
                    
    TaiWo = ['ERZ', 11]
                    
    Fanling = ['ERZ', 12]
                    
    SheungShui = ['ERZ', 13]
                    
    LokMaChau = ['ERZ', 14]
                    
class Line_DCL:
                
    TungChung = ['DCL', 1]
                    
    SunnyBay = ['DCL', 2]
                    
    TsingYi = ['DCL', 3]
                    
    LaiKing = ['DCL', 4]
                    
    NamCheong = ['DCL', 5]
                    
    Olympic = ['DCL', 6]
                    
    Kowloon = ['DCL', 7]
                    
    Central_HongKong = ['DCL', 8]
                    
class Line_SIL:
                
    SouthHorizons = ['SIL', 1]
                    
    LeiTung = ['SIL', 2]
                    
    WongChukHang = ['SIL', 3]
                    
    OceanPark = ['SIL', 4]
                    
    Admiralty = ['SIL', 5]
                    
class Line_DRL:
                
    SunnyBay = ['DRL', 1]
                    
    DisneylandResort = ['DRL', 2]
                    
class Line_AEL:
                
    AsiaWorldExpo = ['AEL', 1]
                    
    Airport = ['AEL', 2]
                    
    TsingYi = ['AEL', 3]
                    
    Kowloon = ['AEL', 4]
                    
    Central_HongKong = ['AEL', 5]
                    
class Station:
            
    TsuenWan = [Line_TWL.TsuenWan,"荃湾"]
                
    TaiWoHau = [Line_TWL.TaiWoHau,"大窝口"]
                
    KwaiHing = [Line_TWL.KwaiHing,"葵兴"]
                
    KwaiFong = [Line_TWL.KwaiFong,"葵芳"]
                
    LaiKing = [Line_TWL.LaiKing,Line_DCL.LaiKing,"荔景"]
                
    MeiFoo = [Line_TWL.MeiFoo,Line_TML.MeiFoo,"美孚"]
                
    LaiChiKok = [Line_TWL.LaiChiKok,"荔枝角"]
                
    CheungShaWan = [Line_TWL.CheungShaWan,"长沙湾"]
                
    ShamShuiPo = [Line_TWL.ShamShuiPo,"深水埗"]
                
    PrinceEdward = [Line_TWL.PrinceEdward,Line_KTL.PrinceEdward,"太子"]
                
    MongKok = [Line_TWL.MongKok,Line_KTL.MongKok,"旺角"]
                
    YauMaTei = [Line_TWL.YauMaTei,Line_KTL.YauMaTei,"油麻地"]
                
    Jordan = [Line_TWL.Jordan,"佐敦"]
                
    TsimShaTsui_EastTsimShaTsui = [Line_TWL.TsimShaTsui_EastTsimShaTsui,Line_TML.TsimShaTsui_EastTsimShaTsui,"尖沙咀/尖东"]
                
    Admiralty = [Line_TWL.Admiralty,Line_ISL.Admiralty,Line_ERL.Admiralty,Line_ERZ.Admiralty,Line_SIL.Admiralty,"金钟"]
                
    Central_HongKong = [Line_TWL.Central_HongKong,Line_ISL.Central_HongKong,Line_DCL.Central_HongKong,Line_AEL.Central_HongKong,"中环/香港"]
                
    KennedyTown = [Line_ISL.KennedyTown,"坚尼地城"]
                
    HKU = [Line_ISL.HKU,"香港大学"]
                
    SaiYingPun = [Line_ISL.SaiYingPun,"西营盘"]
                
    SheungWan = [Line_ISL.SheungWan,"上环"]
                
    WanChai = [Line_ISL.WanChai,"湾仔"]
                
    CausewayBay = [Line_ISL.CausewayBay,"铜锣湾"]
                
    TinHau = [Line_ISL.TinHau,"天后"]
                
    FortressHill = [Line_ISL.FortressHill,"炮台山"]
                
    NorthPoint = [Line_ISL.NorthPoint,Line_TKL.NorthPoint,Line_TKZ.NorthPoint,"北角"]
                
    QuarryBay = [Line_ISL.QuarryBay,Line_TKL.QuarryBay,Line_TKZ.QuarryBay,"鲗鱼涌"]
                
    TaiKoo = [Line_ISL.TaiKoo,"太古"]
                
    SaiWanHo = [Line_ISL.SaiWanHo,"西湾河"]
                
    ShauKeiWan = [Line_ISL.ShauKeiWan,"筲箕湾"]
                
    HengFaChuen = [Line_ISL.HengFaChuen,"杏花邨"]
                
    ChaiWan = [Line_ISL.ChaiWan,"柴湾"]
                
    TiuKengLeng = [Line_KTL.TiuKengLeng,Line_TKL.TiuKengLeng,Line_TKZ.TiuKengLeng,"调景岭"]
                
    YauTong = [Line_KTL.YauTong,Line_TKL.YauTong,Line_TKZ.YauTong,"油塘"]
                
    LamTin = [Line_KTL.LamTin,"蓝田"]
                
    KwunTong = [Line_KTL.KwunTong,"观塘"]
                
    NgauTauKok = [Line_KTL.NgauTauKok,"牛头角"]
                
    KowloonBay = [Line_KTL.KowloonBay,"九龙湾"]
                
    ChoiHung = [Line_KTL.ChoiHung,"彩虹"]
                
    DiamondHill = [Line_KTL.DiamondHill,Line_TML.DiamondHill,"钻石山"]
                
    WongTaiSin = [Line_KTL.WongTaiSin,"黄大仙"]
                
    LokFu = [Line_KTL.LokFu,"乐富"]
                
    KowloonTong = [Line_KTL.KowloonTong,Line_ERL.KowloonTong,Line_ERZ.KowloonTong,"九龙塘"]
                
    ShekKipMei = [Line_KTL.ShekKipMei,"石硖尾"]
                
    HoManTin = [Line_KTL.HoManTin,Line_TML.HoManTin,"何文田"]
                
    Whampoa = [Line_KTL.Whampoa,"黄埔"]
                
    TuenMun = [Line_TML.TuenMun,"屯门"]
                
    SiuHong = [Line_TML.SiuHong,"兆康"]
                
    TinShuiWai = [Line_TML.TinShuiWai,"天水围"]
                
    LongPing = [Line_TML.LongPing,"朗屏"]
                
    YuenLong = [Line_TML.YuenLong,"元朗"]
                
    KamSheungRoad = [Line_TML.KamSheungRoad,"锦上路"]
                
    TsuenWanWest = [Line_TML.TsuenWanWest,"荃湾西"]
                
    NamCheong = [Line_TML.NamCheong,Line_DCL.NamCheong,"南昌"]
                
    Austin = [Line_TML.Austin,"柯士甸"]
                
    HungHom = [Line_TML.HungHom,Line_ERL.HungHom,Line_ERZ.HungHom,"红磡"]
                
    ToKwaWan = [Line_TML.ToKwaWan,"土瓜湾"]
                
    SungWongToi = [Line_TML.SungWongToi,"宋皇台"]
                
    KaiTak = [Line_TML.KaiTak,"启德"]
                
    HinKeng = [Line_TML.HinKeng,"显径"]
                
    TaiWai = [Line_TML.TaiWai,Line_ERL.TaiWai,Line_ERZ.TaiWai,"大围"]
                
    CheKungTemple = [Line_TML.CheKungTemple,"车公庙"]
                
    ShaTinWai = [Line_TML.ShaTinWai,"沙田围"]
                
    CityOne = [Line_TML.CityOne,"第一城"]
                
    ShekMun = [Line_TML.ShekMun,"石门"]
                
    TaiShuiHang = [Line_TML.TaiShuiHang,"大水坑"]
                
    HengOn = [Line_TML.HengOn,"恒安"]
                
    MaOnShan = [Line_TML.MaOnShan,"马鞍山"]
                
    WuKaiSha = [Line_TML.WuKaiSha,"乌溪沙"]
                
    TseungKwanO = [Line_TKL.TseungKwanO,Line_TKZ.TseungKwanO,"将军澳"]
                
    HangHau = [Line_TKL.HangHau,"坑口"]
                
    PoLam = [Line_TKL.PoLam,"宝琳"]
                
    LOHAS1o1Park = [Line_TKZ.LOHAS1o1Park,"康城"]
                
    ExhibitionCentre = [Line_ERL.ExhibitionCentre,Line_ERZ.ExhibitionCentre,"会展"]
                
    MongKokEast = [Line_ERL.MongKokEast,Line_ERZ.MongKokEast,"旺角东"]
                
    ShaTin = [Line_ERL.ShaTin,Line_ERZ.ShaTin,"沙田"]
                
    FoTan = [Line_ERL.FoTan,Line_ERZ.FoTan,"火炭"]
                
    University = [Line_ERL.University,Line_ERZ.University,"大学"]
                
    TaiPoMarket = [Line_ERL.TaiPoMarket,Line_ERZ.TaiPoMarket,"大埔墟"]
                
    TaiWo = [Line_ERL.TaiWo,Line_ERZ.TaiWo,"太和"]
                
    Fanling = [Line_ERL.Fanling,Line_ERZ.Fanling,"粉岭"]
                
    SheungShui = [Line_ERL.SheungShui,Line_ERZ.SheungShui,"上水"]
                
    LoWu = [Line_ERL.LoWu,"罗湖"]
                
    LokMaChau = [Line_ERZ.LokMaChau,"落马洲"]
                
    TungChung = [Line_DCL.TungChung,"东涌"]
                
    SunnyBay = [Line_DCL.SunnyBay,Line_DRL.SunnyBay,"欣澳"]
                
    TsingYi = [Line_DCL.TsingYi,Line_AEL.TsingYi,"青衣"]
                
    Olympic = [Line_DCL.Olympic,"奥运"]
                
    Kowloon = [Line_DCL.Kowloon,Line_AEL.Kowloon,"九龙"]
                
    SouthHorizons = [Line_SIL.SouthHorizons,"海怡半岛"]
                
    LeiTung = [Line_SIL.LeiTung,"利东"]
                
    WongChukHang = [Line_SIL.WongChukHang,"黄竹坑"]
                
    OceanPark = [Line_SIL.OceanPark,"海洋公园"]
                
    DisneylandResort = [Line_DRL.DisneylandResort,"迪士尼"]
                
    AsiaWorldExpo = [Line_AEL.AsiaWorldExpo,"博览馆"]
                
    Airport = [Line_AEL.Airport,"机场"]
                
DESCRIPTION = [['TsuenWan', '数码服务站：A出口\n饮水机：车站大堂C出口（非付费区）'], ['TaiWoHau', '数码服务站：B出口'], ['KwaiHing', '数码服务站：A/D出口'], ['KwaiFong', '数码服务站：A/D出口\n饮水机：车站大堂C出口（非付费区）'], ['LaiKing', '洗手间：车站大堂（付费区）\n哺乳室：车站大堂（付费区）\n数码服务站：车站大堂\n'], ['MeiFoo', '洗手间：屯马线车站大堂（付费区）\n数码服务站：A出口\n饮水机：B出口（非付费区）'], ['LaiChiKok', '数码服务站：A出口'], ['CheungShaWan', '数码服务站：C出口'], ['ShamShuiPo', '数码服务站：C出口'], ['PrinceEdward', '洗手间：A出口（付费区）\n数码服务站：车站大堂\n饮水机：A出口（非付费区）'], ['MongKok', '洗手间：A出口（付费区）\n数码服务站：E出口'], ['YauMaTei', '洗手间：C出口（付费区）\n哺乳室：C出口（付费区）\n数码服务站：D出口'], ['Jordan', '数码服务站：C出口'], ['TsimShaTsui_EastTsimShaTsui', '洗手间：尖沙咀站E出口（非付费区） 尖东站车站大堂（付费区）\n哺乳室：尖沙咀站E出口（非付费区）\n数码服务站：尖沙咀站C出口 尖东站车站大堂东侧\n饮水机：尖东站P1出口（非付费区）'], ['Admiralty', '洗手间：车站大堂L1层/L5层/F出口（付费区）\n哺乳室：F出口（付费区）\n数码服务站：D出口\n饮水机：B出口（非付费区）'], ['Central_HongKong', '洗手间：中环站车站大堂L2层A出口（付费区） 香港站车站大堂G层E出口/L1层/L2层（非付费区）\n哺乳室：中环站车站大堂L2层A出口（付费区）\n数码服务站：中环站A出口 香港站东涌线车站大堂L3层（F出口旁）'], ['KennedyTown', '洗手间：A出口（非付费区）\n数码服务站：C出口'], ['HKU', '洗手间：B出口（付费区）\n数码服务站：B出口'], ['SaiYingPun', '洗手间：B出口（付费区）\n数码服务站：A出口'], ['SheungWan', '洗手间：E出口（付费区）\n数码服务站：车站大堂中部'], ['WanChai', '数码服务站：车站大堂'], ['CausewayBay', '数码服务站：A出口'], ['TinHau', '数码服务站：B出口'], ['FortressHill', '数码服务站：B出口'], ['NorthPoint', '洗手间：B出口（付费区）\n哺乳室：B出口（付费区）\n数码服务站：A出口\n饮水机：B出口（非付费区）'], ['QuarryBay', '洗手间：A出口（付费区）\n数码服务站：C出口'], ['TaiKoo', '数码服务站：D出口'], ['SaiWanHo', '数码服务站：A出口'], ['ShauKeiWan', '数码服务站：B出口和C出口附近'], ['HengFaChuen', '数码服务站：A出口'], ['ChaiWan', '数码服务站：车站大堂\n饮水机：D出口（非付费区）'], ['TiuKengLeng', '洗手间：车站大堂（付费区）\n哺乳室：车站大堂（付费区）\n数码服务站：A出口\n饮水机：B出口（非付费区）'], ['YauTong', '洗手间：车站大堂（付费区）\n哺乳室：车站大堂（付费区）\n数码服务站：车站大堂中部'], ['LamTin', '数码服务站：B出口'], ['KwunTong', '数码服务站：B出口'], ['NgauTauKok', '洗手间：车站大堂（付费区）\n数码服务站：A出口'], ['KowloonBay', '数码服务站：C出口'], ['ChoiHung', '数码服务站：C出口\n饮水机：A1出口（非付费区）'], ['DiamondHill', '洗手间：屯马线车站大堂（付费区）\n哺乳室：屯马线车站大堂（付费区）\n数码服务站：A出口\n饮水机：A2出口（非付费区）'], ['WongTaiSin', '数码服务站：E出口'], ['LokFu', '数码服务站：车站大堂'], ['KowloonTong', '洗手间：东铁线车站大堂北侧（付费区）\n数码服务站：B出口'], ['ShekKipMei', '数码服务站：A出口对面'], ['HoManTin', '洗手间：B出口（付费区）\n数码服务站：A出口\n饮水机：A出口（非付费区）'], ['Whampoa', '洗手间：D出口（付费区）\n数码服务站：B/C出口'], ['TuenMun', '洗手间：F出口（付费区）\n数码服务站：C出口'], ['SiuHong', '洗手间：A出口（付费区）\n数码服务站：E出口'], ['TinShuiWai', '洗手间：C出口（付费区）\n数码服务站：D出口\n饮水机：E3出口（非付费区）'], ['LongPing', '洗手间：车站大堂（付费区）\n数码服务站：B出口'], ['YuenLong', '洗手间：车站大堂（付费区）\n数码服务站：F出口'], ['KamSheungRoad', '洗手间：车站大堂（付费区）\n数码服务站：A出口'], ['TsuenWanWest', '洗手间：车站大堂（付费区）\n数码服务站：E出口'], ['NamCheong', '洗手间：A出口（付费区）\n数码服务站：A出口\n饮水机：A出口（非付费区）'], ['Austin', '洗手间：C出口（付费区）\n数码服务站：A出口\n饮水机：C出口（非付费区）'], ['HungHom', '洗手间：车站大堂U2层/U3层（非付费区）和屯马线站台\n数码服务站：C出口'], ['ToKwaWan', '洗手间：B出口（付费区）\n哺乳室：B出口（付费区）\n数码服务站：车站大堂中部\n饮水机：A出口（非付费区）'], ['SungWongToi', '洗手间：D出口（付费区）\n哺乳室：D出口（付费区）\n数码服务站：A出口\n饮水机：A出口（非付费区）'], ['KaiTak', '洗手间：C出口（付费区）\n哺乳室：C出口（付费区）\n数码服务站：D出口\n饮水机：A出口（非付费区）'], ['HinKeng', '洗手间：车站大堂（付费区）\n哺乳室：车站大堂（付费区）\n数码服务站：A出口'], ['TaiWai', '洗手间：B出口（付费区）\n数码服务站：A出口\nC出口（非付费区）'], ['CheKungTemple', '洗手间：车站大堂（付费区）\n数码服务站：C出口'], ['ShaTinWai', '洗手间：车站大堂（付费区）\n数码服务站：A出口'], ['CityOne', '洗手间：车站大堂（付费区）\n数码服务站：C/D出口'], ['ShekMun', '洗手间：车站大堂（付费区）'], ['TaiShuiHang', '洗手间：车站大堂（付费区）\n数码服务站：车站控制室旁\n饮水机：A出口（非付费区）'], ['HengOn', '洗手间：车站大堂（付费区）\n数码服务站：C出口'], ['MaOnShan', '洗手间：车站大堂（付费区）\n数码服务站：B出口'], ['WuKaiSha', '洗手间：车站大堂（付费区）\n数码服务站：A出口'], ['TseungKwanO', '数码服务站：B2出口'], ['HangHau', '数码服务站：B出口\n饮水机：A出口（非付费区）'], ['PoLam', '数码服务站：B出口'], ['LOHAS1o1Park', '数码服务站：C出口'], ['ExhibitionCentre', '洗手间：B出口（付费区）\n哺乳室：B出口（付费区）\n数码服务站：A出口\n饮水机：A出口（非付费区）'], ['MongKokEast', '洗手间：C出口（付费区）\n数码服务站：D出口'], ['ShaTin', '洗手间：车站大堂（付费区）\n数码服务站：A出口'], ['FoTan', '洗手间：A出口（付费区）\n数码服务站：A出口'], ['University', '洗手间：B出口（付费区）\n数码服务站：B出口'], ['TaiPoMarket', '洗手间：A出口（付费区）\n数码服务站：B出口\n饮水机：B出口（非付费区）'], ['TaiWo', '洗手间：A出口（付费区）\n数码服务站：A出口'], ['Fanling', '洗手间：车站大堂（付费区）\n数码服务站：车站大堂'], ['SheungShui', '洗手间：车站大堂（付费区）\n数码服务站：B出口'], ['LoWu', '洗手间：站台（付费区）和抵港大堂层（非付费区）\n数码服务站：入境大堂（2楼）和出境大堂（地下）'], ['LokMaChau', '洗手间：抵港大堂层（非付费区）和离港大堂层（付费区）\n数码服务站：到境大堂（2楼）和票务大堂（3楼）'], ['TungChung', '数码服务站：A出口和B出口附近\n饮水机：D出口（非付费区）'], ['SunnyBay', '洗手间：迪士尼线迪士尼方向3号站台'], ['TsingYi', '洗手间：车站大堂U2层和U4层（非付费区）\n数码服务站：车站大堂\n饮水机：C出口（非付费区）'], ['Olympic', '数码服务站：C出口和D出口附近'], ['Kowloon', '洗手间：车站大堂G层B出口和L2层（非付费区）\n数码服务站：车站大堂'], ['SouthHorizons', '洗手间：车站大堂（付费区）\n数码服务站：C出口\n饮水机：B出口（非付费区）'], ['LeiTung', '洗手间：车站大堂（付费区）\n数码服务站：A出口'], ['WongChukHang', '洗手间：车站大堂（付费区）\n数码服务站：A出口'], ['OceanPark', '洗手间：车站大堂（付费区）\n数码服务站：B出口'], ['DisneylandResort', '洗手间：迪士尼线欣澳方向1号站台'], ['AsiaWorldExpo', '数码服务站：A出口'], ['Airport', '数码服务站：L5层入境站台']]
            