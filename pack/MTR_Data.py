ALL_LINE_LIST = ["TWL","ISL","KTL","TML","TKL","TKZ","ERL","ERZ","DCL","SIL","DRL","AEL"]

ALL_LINE_DICT = {
                "荃湾线":"TWL",
                "港岛线":"ISL",
                "观塘线":"KTL",
                "屯马线":"TML",
                "将军澳线（主线）":"TKL",
                "将军澳线（支线）":"TKZ",
                "东铁线（主线）":"ERL",
                "东铁线（支线）":"ERZ",
                "东涌线":"DCL",
                "南港岛线":"SIL",
                "迪士尼线":"DRL",
                "机场快线":"AEL"
                }

ABOVE_ZERO_DIRECTION = {
                "TWL": "开往 荃湾 方向",
                "ISL": "开往 坚尼地城 方向",
                "KTL": "开往 调景岭 方向",
                "TML": "开往 屯门 方向",
                "TKL": "开往 北角 方向",
                "TKZ": "开往 北角 方向",
                "ERL": "开往 金钟 方向",
                "ERZ": "开往 金钟 方向",
                "DCL": "开往 东涌 方向",
                "SIL": "开往 海怡半岛 方向",
                "DRL": "开往 欣澳 方向",
                "AEL": "开往 博览馆 方向"
                }

BELOW_ZERO_DIRECTION = {
                "TWL": "开往 中环 方向",
                "ISL": "开往 柴湾 方向",
                "KTL": "开往 黄埔 方向",
                "TML": "开往 乌溪沙 方向",
                "TKL": "开往 宝琳 方向",
                "TKZ": "开往 康城 方向",
                "ERL": "开往 罗湖 方向",
                "ERZ": "开往 落马洲 方向",
                "DCL": "开往 香港 方向",
                "SIL": "开往 金钟 方向",
                "DRL": "开往 迪士尼 方向",
                "AEL": "开往 香港 方向"
                }

TIME_DICT = {"TWL":"首班车  06:00\n末班车  次日01:22",
             "ISL": "首班车  05:55\n末班车  次日00:35",
             "KTL": "首班车  06:07\n末班车  次日01:08",
             "TML": "首班车  05:38\n末班车  次日01:22",
             "TKL": "首班车  05:57\n末班车  次日01:26",
             "TKZ": "首班车  05:57\n末班车  次日01:26",
             "ERL": "首班车  05:28\n末班车  次日01:09",
             "ERZ": "首班车  05:28\n末班车  次日01:09",
             "DCL": "首班车  05:59\n末班车  次日01:09",
             "SIL": "首班车  06:00\n末班车  次日01:14",
             "DRL": "首班车  06:15\n末班车  次日00:45",
             "AEL": "首班车  05:50\n末班车  次日01:13"
         }

RGB_DICT = {"TWL": "rgb(226,35,26)",
            "ISL": "rgb(0,113,206)",
            "KTL": "rgb(0,175,65)",
            "TML": "rgb(154,56,32)",
            "TKL": "rgb(163,94,181)",
            "TKZ": "rgb(163,94,181)",
            "ERL": "rgb(97,180,228)",
            "ERZ": "rgb(97,180,228)",
            "DCL": "rgb(243,139,0)",
            "SIL": "rgb(182,189,0)",
            "DRL": "rgb(231,119,203)",
            "AEL": "rgb(0,112,120)"
            }

BRANCH_LINE_LIST = [
    ["TKL","TKZ"],
    ["ERL","ERZ"]
    ]

class TsuenWanLine:
    """荃湾线"""
    TsuenWan_TWL = ["TWL",1]
    TaiWoHau_TWL = ["TWL",2]
    KwaiHing_TWL = ["TWL",3]
    KwaiFong_TWL = ["TWL",4]
    LaiKing_TWL = ["TWL",5]
    MeiFoo_TWL = ["TWL",6]
    LaiChiKok_TWL = ["TWL",7]
    CheungShaWan_TWL = ["TWL",8]
    ShamShuiPo_TWL = ["TWL",9]
    PrinceEdward_TWL = ["TWL",10]
    MongKok_TWL = ["TWL",11]
    YauMaTei_TWL = ["TWL",12]
    Jordan_TWL = ["TWL",13]
    TsimShaTsui_TWL = ["TWL",14]
    Admiralty_TWL = ["TWL",15]
    Central_TWL = ["TWL",16]
    
class IslandLine:
    """港岛线"""
    KennedyTown_ISL = ["ISL",1]
    HongkongUniversity_ISL = ["ISL",2]
    SaiYingPun_ISL = ["ISL",3]
    SheungWan_ISL = ["ISL",4]
    Central_ISL = ["ISL",5]
    Admiralty_ISL = ["ISL",6]
    WanChai_ISL = ["ISL",7]
    CausewayBay_ISL = ["ISL",8]
    TinHau_ISL = ["ISL",9]
    FortressHill_ISL = ["ISL",10]
    NorthPoint_ISL = ["ISL",11]
    QuarryBay_ISL = ["ISL",12]
    TaiKoo_ISL = ["ISL",13]
    SaiWanHo_ISL = ["ISL",14]
    ShauKeiWan_ISL = ["ISL",15]
    HengFaChuen_ISL = ["ISL",16]
    ChaiWan_ISL = ["ISL",17]
    
class KwunTongLine:
    """观塘线"""
    TiuKengLeng_KTL = ["KTL",1]
    YauTong_KTL = ["KTL",2]
    LamTin_KTL = ["KTL",3]
    KwunTong_KTL = ["KTL",4]
    NgauTauKok_KTL = ["KTL",5]
    KowloonBay_KTL = ["KTL",6]
    ChoiHung_KTL = ["KTL",7]
    DiamondHill_KTL = ["KTL",8]
    WongTaiSin_KTL = ["KTL",9]
    LokFu_KTL = ["KTL",10]
    KowloonTong_KTL = ["KTL",11]
    ShekKipMei_KTL = ["KTL",12]
    PrinceEdward_KTL = ["KTL",13]
    MongKok_KTL = ["KTL",14]
    YauMaTei_KTL = ["KTL",15]
    HoManTin_KTL = ["KTL",16]
    Whampoa_KTL = ["KTL",17]
    
class TuenMaLine:
    """屯马线"""
    TuenMun_TML = ["TML",1]
    SiuHong_TML = ["TML",2]
    TinShuiWai_TML = ["TML",3]
    LongPing_TML = ["TML",4]
    YuenLong_TML = ["TML",5]
    KamSheungRoad_TML = ["TML",6]
    TsuenWanWest_TML = ["TML",7]
    MeiFoo_TML = ["TML",8]
    NamCheong_TML = ["TML",9]
    Austin_TML = ["TML",10]
    EastTsimShaTsui_TML = ["TML",11]
    HungHom_TML = ["TML",12]
    HoManTin_TML = ["TML",13]
    ToKwaWan_TML = ["TML",14]
    SungWongToi_TML = ["TML",15]
    KaiTak_TML = ["TML",16]
    DiamondHill_TML = ["TML",17]
    HinKeng_TML = ["TML",18]
    TaiWai_TML = ["TML",19]
    CheKungTemple_TML = ["TML",20]
    ShaTinWai_TML = ["TML",21]
    CityOne_TML = ["TML",22]
    ShekMun_TML = ["TML",23]
    TaiShuiHang_TML = ["TML",24]
    HengOn_TML = ["TML",25]
    MaOnShan_TML = ["TML",26]
    WuKaiSha_TML = ["TML",27]
    
class TseungKwanOLine:
    """将军澳线（主线）"""
    NorthPoint_TKL = ["TKL",1]
    QuarryBay_TKL = ["TKL",2]
    YauTong_TKL = ["TKL",3]
    TiuKengLeng_TKL = ["TKL",4]
    TseungKwanO_TKL = ["TKL",5]
    HangHau_TKL = ["TKL",6]
    PoLam_TKL = ["TKL",7]
    
class TseungKwanOLineZ:
    """将军澳线（支线）"""
    NorthPoint_TKZ = ["TKZ",1]
    QuarryBay_TKZ = ["TKZ",2]
    YauTong_TKZ = ["TKZ",3]
    TiuKengLeng_TKZ = ["TKZ",4]
    TseungKwanO_TKZ = ["TKZ",5]
    LOHASPark_TKZ = ["TKZ",6]
    
class EastRailLine:
    """东铁线（主线）"""
    Admiralty_ERL = ["ERL",1]
    ExhibitionCentre_ERL = ["ERL",2]
    HungHom_ERL = ["ERL",3]
    MongKokEast_ERL = ["ERL",4]
    KowloonTong_ERL = ["ERL",5]
    TaiWai_ERL = ["ERL",6]
    ShaTin_ERL = ["ERL",7]
    FoTan_ERL = ["ERL",8]
    University_ERL = ["ERL",9]
    TaiPoMarket_ERL = ["ERL",10]
    TaiWo_ERL = ["ERL",11]
    Fanling_ERL = ["ERL",12]
    SheungShui_ERL = ["ERL",13]
    LoWu_ERL = ["ERL",14]
    
class EastRailLineZ:
    """东铁线（支线）"""
    Admiralty_ERZ = ["ERZ",1]
    ExhibitionCentre_ERZ = ["ERZ",2]
    HungHom_ERZ = ["ERZ",3]
    MongKokEast_ERZ = ["ERZ",4]
    KowloonTong_ERZ = ["ERZ",5]
    TaiWai_ERZ = ["ERZ",6]
    ShaTin_ERZ = ["ERZ",7]
    FoTan_ERZ = ["ERZ",8]
    University_ERZ = ["ERZ",9]
    TaiPoMarket_ERZ = ["ERZ",10]
    TaiWo_ERZ = ["ERZ",11]
    Fanling_ERZ = ["ERZ",12]
    SheungShui_ERZ = ["ERZ",13]
    LokMaChau_ERZ = ["ERZ",14]
    
class DongChungLine:
    """东涌线"""
    TungChung_DCL = ["DCL",1]
    SunnyBay_DCL = ["DCL",2]
    TsingYi_DCL = ["DCL",3]
    LaiKing_DCL = ["DCL",4]
    NamCheong_DCL = ["DCL",5]
    Olympic_DCL = ["DCL",6]
    Kowloon_DCL = ["DCL",7]
    HongKong_DCL = ["DCL",8]
    
class SouthIslandLine:
    """南港岛线"""
    SouthHorizons_SIL = ["SIL",1]
    LeiTung_SIL = ["SIL",2]
    WongChukHang_SIL = ["SIL",3]
    OceanPark_SIL = ["SIL",4]
    Admiralty_SIL = ["SIL",5]
    
class DisneylandResortLine:
    """迪士尼线"""
    SunnyBay_DRL = ["DRL",1]
    DisneylandResort_DRL = ["DRL",2]
    
class AirportExpress:
    """机场快线"""
    AsiaWorldExpo_AEL = ["AEL",1]
    Airport_AEL = ["AEL",2]
    TsingYi_AEL = ["AEL",3]
    Kowloon_AEL = ["AEL",4]
    HongKong_AEL = ["AEL",5]
    
class Station:
    """站点"""
    TsuenWan = [TsuenWanLine.TsuenWan_TWL,"荃湾"]
    TaiWoHau = [TsuenWanLine.TaiWoHau_TWL,"大窝口"]
    KwaiHing = [TsuenWanLine.KwaiHing_TWL,"葵兴"]
    KwaiFong = [TsuenWanLine.KwaiFong_TWL,"葵芳"]
    LaiKing = [TsuenWanLine.LaiKing_TWL,DongChungLine.LaiKing_DCL,"荔景"]
    MeiFoo = [TsuenWanLine.MeiFoo_TWL,TuenMaLine.MeiFoo_TML,"美孚"]
    LaiChiKok = [TsuenWanLine.LaiChiKok_TWL,"荔枝角"]
    CheungShaWan = [TsuenWanLine.CheungShaWan_TWL,"长沙湾"]
    ShamShuiPo = [TsuenWanLine.ShamShuiPo_TWL,"深水埗"]
    PrinceEdward = [TsuenWanLine.PrinceEdward_TWL,KwunTongLine.PrinceEdward_KTL,"太子"]
    MongKok = [TsuenWanLine.MongKok_TWL,KwunTongLine.MongKok_KTL,"旺角"]
    YauMaTei = [TsuenWanLine.YauMaTei_TWL,KwunTongLine.YauMaTei_KTL,"油麻地"]
    Jordan = [TsuenWanLine.Jordan_TWL,"佐敦"]
    TsimShaTsui_EastTsimShaTsui = [TsuenWanLine.TsimShaTsui_TWL,TuenMaLine.EastTsimShaTsui_TML,"尖沙咀/尖东"]
    Admiralty = [TsuenWanLine.Admiralty_TWL,IslandLine.Admiralty_ISL,SouthIslandLine.Admiralty_SIL,EastRailLine.Admiralty_ERL,EastRailLineZ.Admiralty_ERZ,"金钟"]
    Central_HongKong = [TsuenWanLine.Central_TWL,IslandLine.Central_ISL,DongChungLine.HongKong_DCL,AirportExpress.HongKong_AEL,"中环/香港"]
    KennedyTown = [IslandLine.KennedyTown_ISL,"坚尼地城"]
    HongkongUniversity = [IslandLine.HongkongUniversity_ISL,"香港大学"]
    SaiYingPun = [IslandLine.SaiYingPun_ISL,"西营盘"]
    SheungWan = [IslandLine.SheungWan_ISL,"上环"]
    WanChai = [IslandLine.WanChai_ISL,"湾仔"]
    CausewayBay = [IslandLine.CausewayBay_ISL,"铜锣湾"]
    TinHau = [IslandLine.TinHau_ISL,"天后"]
    FortressHill = [IslandLine.FortressHill_ISL,"炮台山"]
    NorthPoint = [IslandLine.NorthPoint_ISL,TseungKwanOLine.NorthPoint_TKL,TseungKwanOLineZ.NorthPoint_TKZ,"北角"]
    QuarryBay = [IslandLine.QuarryBay_ISL,TseungKwanOLine.QuarryBay_TKL,TseungKwanOLineZ.QuarryBay_TKZ,"鲗鱼涌"]
    TaiKoo = [IslandLine.TaiKoo_ISL,"太古"]
    SaiWanHo = [IslandLine.SaiWanHo_ISL,"西湾河"]
    ShauKeiWan = [IslandLine.ShauKeiWan_ISL,"筲箕湾"]
    HengFaChuen = [IslandLine.HengFaChuen_ISL,"杏花邨"]
    ChaiWan = [IslandLine.ChaiWan_ISL,"柴湾"]
    TiuKengLeng = [KwunTongLine.TiuKengLeng_KTL,TseungKwanOLine.TiuKengLeng_TKL,TseungKwanOLineZ.TiuKengLeng_TKZ,"调景岭"]
    YauTong = [KwunTongLine.YauTong_KTL,TseungKwanOLine.YauTong_TKL,TseungKwanOLineZ.YauTong_TKZ,"油塘"]
    LamTin = [KwunTongLine.LamTin_KTL,"蓝田"]
    KwunTong = [KwunTongLine.KwunTong_KTL,"观塘"]
    NgauTauKok = [KwunTongLine.NgauTauKok_KTL,"牛头角"]
    KowloonBay = [KwunTongLine.KowloonBay_KTL,"九龙湾"]
    ChoiHung = [KwunTongLine.ChoiHung_KTL,"彩虹"]
    DiamondHill = [KwunTongLine.DiamondHill_KTL,TuenMaLine.DiamondHill_TML,"钻石山"]
    WongTaiSin = [KwunTongLine.WongTaiSin_KTL,"黄大仙"]
    LokFu = [KwunTongLine.LokFu_KTL,"乐富"]
    KowloonTong = [KwunTongLine.KowloonTong_KTL,EastRailLine.KowloonTong_ERL,EastRailLineZ.KowloonTong_ERZ,"九龙塘"]
    ShekKipMei = [KwunTongLine.ShekKipMei_KTL,"石硖尾"]
    HoManTin = [KwunTongLine.HoManTin_KTL,TuenMaLine.HoManTin_TML,"何文田"]
    Whampoa = [KwunTongLine.Whampoa_KTL,"黄埔"]
    TuenMun = [TuenMaLine.TuenMun_TML,"屯门"]
    SiuHong = [TuenMaLine.SiuHong_TML,"兆康"]
    TinShuiWai = [TuenMaLine.TinShuiWai_TML,"天水围"]
    LongPing = [TuenMaLine.LongPing_TML,"朗屏"]
    YuenLong = [TuenMaLine.YuenLong_TML,"元朗"]
    KamSheungRoad = [TuenMaLine.KamSheungRoad_TML,"锦上路"]
    TsuenWanWest = [TuenMaLine.TsuenWanWest_TML,"荃湾西"]
    NamCheong = [TuenMaLine.NamCheong_TML,DongChungLine.NamCheong_DCL,"南昌"]
    Austin = [TuenMaLine.Austin_TML,"柯士甸"]
    HungHom = [TuenMaLine.HungHom_TML,EastRailLine.HungHom_ERL,EastRailLineZ.HungHom_ERZ,"红磡"]
    ToKwaWan = [TuenMaLine.ToKwaWan_TML,"土瓜湾"]
    SungWongToi = [TuenMaLine.SungWongToi_TML,"宋皇台"]
    KaiTak = [TuenMaLine.KaiTak_TML,"启德"]
    HinKeng = [TuenMaLine.HinKeng_TML,"显径"]
    TaiWai = [TuenMaLine.TaiWai_TML,EastRailLine.TaiWai_ERL,EastRailLineZ.TaiWai_ERZ,"大围"]
    CheKungTemple = [TuenMaLine.CheKungTemple_TML,"车公庙"]
    ShaTinWai = [TuenMaLine.ShaTinWai_TML,"沙田围"]
    CityOne = [TuenMaLine.CityOne_TML,"第一城"]
    ShekMun = [TuenMaLine.ShekMun_TML,"石门"]
    TaiShuiHang = [TuenMaLine.TaiShuiHang_TML,"大水坑"]
    HengOn = [TuenMaLine.HengOn_TML,"恒安"]
    MaOnShan = [TuenMaLine.MaOnShan_TML,"马鞍山"]
    WuKaiSha = [TuenMaLine.WuKaiSha_TML,"乌溪沙"]
    TseungKwanO = [TseungKwanOLine.TseungKwanO_TKL,TseungKwanOLineZ.TseungKwanO_TKZ,"将军澳"]
    HangHau = [TseungKwanOLine.HangHau_TKL,"坑口"]
    PoLam = [TseungKwanOLine.PoLam_TKL,"宝琳"]
    LOHASPark = [TseungKwanOLineZ.LOHASPark_TKZ,"康城"]
    ExhibitionCentre = [EastRailLine.ExhibitionCentre_ERL,EastRailLineZ.ExhibitionCentre_ERZ,"会展"]
    MongKokEast = [EastRailLine.MongKokEast_ERL,EastRailLineZ.MongKokEast_ERZ,"旺角东"]
    ShaTin = [EastRailLine.ShaTin_ERL,EastRailLineZ.ShaTin_ERZ,"沙田"]
    FoTan = [EastRailLine.FoTan_ERL,EastRailLineZ.FoTan_ERZ,"火炭"]
    University = [EastRailLine.University_ERL,EastRailLineZ.University_ERZ,"大学"]
    TaiPoMarket = [EastRailLine.TaiPoMarket_ERL,EastRailLineZ.TaiPoMarket_ERZ,"大埔墟"]
    TaiWo = [EastRailLine.TaiWo_ERL,EastRailLineZ.TaiWo_ERZ,"太和"]
    Fanling = [EastRailLine.Fanling_ERL,EastRailLineZ.Fanling_ERZ,"粉岭"]
    SheungShui = [EastRailLine.SheungShui_ERL,EastRailLineZ.SheungShui_ERZ,"上水"]
    LoWu = [EastRailLine.LoWu_ERL,"罗湖"]
    LokMaChau = [EastRailLineZ.LokMaChau_ERZ,"落马洲"]
    TungChung = [DongChungLine.TungChung_DCL,"东涌"]
    SunnyBay = [DongChungLine.SunnyBay_DCL,DisneylandResortLine.SunnyBay_DRL,"欣澳"]
    TsingYi = [DongChungLine.TsingYi_DCL,AirportExpress.TsingYi_AEL,"青衣"]
    Olympic = [DongChungLine.Olympic_DCL,"奥运"]
    Kowloon = [DongChungLine.Kowloon_DCL,AirportExpress.Kowloon_AEL,"九龙"]
    SouthHorizons = [SouthIslandLine.SouthHorizons_SIL,"海怡半岛"]
    LeiTung = [SouthIslandLine.LeiTung_SIL,"利东"]
    WongChukHang = [SouthIslandLine.WongChukHang_SIL,"黄竹坑"]
    OceanPark = [SouthIslandLine.OceanPark_SIL,"海洋公园"]
    DisneylandResort = [DisneylandResortLine.DisneylandResort_DRL,"迪士尼"]
    AsiaWorldExpo = [AirportExpress.AsiaWorldExpo_AEL,"博览馆"]
    Airport = [AirportExpress.Airport_AEL,"机场"]