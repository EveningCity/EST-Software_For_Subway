ALL_LINE_LIST = ["1","2","4","6","S5","XP","XPZ","XR","XG","HL1","HL2","HL5","HL8","HL16","HL17","HL20","HL20SW","HLS3"]
ALL_LINE_DICT = {
                "1号线（凤岗线）":"1",
                "2号线（东西线）":"2",
                "4号线（富乐线）":"4",
                "6号线（嘉文线）":"6",
                "S5号线（进武线）":"S5",
                "新平城际（支线）":"XPZ",
                "新平城际（主线）":"XP",
                "郗县捷运绿线":"XG",
                "郗县捷运红线":"XR",
                "互利1号线":"HL1",
                "互利2号线":"HL2",
                "互利5号线":"HL5",
                "互利8号线":"HL8",
                "互利16号线":"HL16",
                "互利17号线":"HL17",
                "互利20号线":"HL20",
                "互利20号线（商务特急）":"HL20SW",
                "互利S3号线":"HLS3"
                }

ABOVE_ZERO_DIRECTION = {
                "1": "开往 凤岗里 方向",
                "2": "开往 市医学院 方向",
                "4": "开往 安平财大 方向",
                "6": "开往 流芳 方向",
                "S5": "开往 九龙湖街 方向",
                "XP": "开往 黄龙国际机场 方向",
                "XPZ": "开往 黄龙国际机场 方向",
                "XR": "内环 方向",
                "XG": "开往 荷花池头 方向",
                "HL1": "开往 互利新港 方向",
                "HL2": "开往 祖庙 方向",
                "HL5": "开往 东方路 方向",
                "HL8": "开往 海底神殿 方向",
                "HL16": "开往 黄龙国际机场 方向",
                "HL17": "开往 悬树 方向",
                "HL20": "开往 互利南站 方向",
                "HL20SW": "开往 互利南站 方向",
                "HLS3": "开往 互利东站 方向"
                }

BELOW_ZERO_DIRECTION = {
                "1": "开往 体育中心 方向",
                "2": "开往 明华路 方向",
                "4": "开往 郗县/下港 方向",
                "6": "开往 九重天 方向",
                "S5": "开往 五岔路口 方向",
                "XP": "开往 新权南山 方向",
                "XPZ": "开往 方舟广场 方向",
                "XR": "外环 方向",
                "XG": "开往 漫水桥村 方向",
                "HL1": "开往 互利东站 方向",
                "HL2": "开往 星湖 方向",
                "HL5": "开往 滨海家园 方向",
                "HL8": "开往 弗卢伊特村 方向",
                "HL16": "开往 互利北站 方向",
                "HL17": "开往 芫荽 方向",
                "HL20": "开往 黄兴 方向",
                "HL20SW": "开往 五岔路口 方向",
                "HLS3": "开往 滨海家园 方向"
                }

TIME_DICT = {"1":"首班车  6:00\n末班车  23:00\n（小交路约3分钟/班，大交路约5分钟/班）",      
            "2":"首班车  6:00\n末班车  23:00\n（小交路约3分钟/班，大交路约5分钟/班）",
            "4":"首班车  6:00\n末班车  23:00\n（小交路约3分钟/班，大交路约5分钟/班）",
            "6":"首班车  6:00\n末班车  23:00\n（小交路约3分钟/班，大交路约5分钟/班）",
            "S5":"首班车  6:00\n末班车  00:00\n（约5分钟/班）",
            "XP":"首班车  7:00\n末班车  23:00\n（约5分钟/班）",
            "XPZ":"首班车  6:00\n末班车  23:00\n（约5分钟/班）",
            "XR":"首班车  6:00\n末班车  23:00\n（约2分钟/班）",
            "XG":"首班车  6:00\n末班车  23:00\n（约2分钟/班）",
            "HL1":"首班车  6:00\n末班车  23:00\n（约3分钟/班）",
            "HL2":"首班车  6:00\n末班车  23:00\n（约2分钟/班）",
            "HL5":"首班车  6:00\n末班车  23:00\n（约3分钟/班）",
            "HL8":"首班车  6:00\n末班车  23:00\n（约3分钟/班）",
            "HL16":"首班车  6:00\n末班车  00:00\n（约5分钟/班）",
            "HL17":"首班车  6:00\n末班车  23:00\n（约5分钟/班）",
            "HL20":"首班车  6:00\n末班车  23:00\n（约5分钟/班）",
            "HL20SW":"首班车  7:00\n末班车  22:00\n（约5分钟/班）",
            "HLS3":"首班车  6:00\n末班车  23:00\n（约3分钟/班）"
         }

RGB_DICT = {"1":"rgb(201,49,43)",
            "2":"rgb(220,159,70)",
            "4":"rgb(102,184,156)",
            "6":"rgb(127,0,255)",
            "S5":"rgb(25,86,94)",
            "XP":"rgb(255,85,153)",
            "XPZ":"rgb(255,85,153)",
            "XR":"rgb(160,37,42)",
            "XG":"rgb(0,117,75)",
            "HL1":"rgb(208,23,34)",
            "HL2":"rgb(0,0,139)",
            "HL5":"rgb(221,0,102)",
            "HL8":"rgb(41,109,35)",
            "HL16":"rgb(107,184,177)",
            "HL17":"rgb(255,0,204)",
            "HL20":"rgb(188,111,55)",
            "HL20SW":"rgb(108,52,97)",
            "HLS3":"rgb(107,142,35)"
            }

class LineXP:
    """新平城际"""
    HLIntlAirportXP = ["XP",1]
    JiulonghuStreetXP = ["XP",2]
    SangzhiXP = ["XP",3]
    SinkholeVillageXP = ["XP",4]
    FredsBeachXP = ["XP",5]
    ShuangliNewTownEastXP = ["XP",6]
    BinhaiWestAveneXP = ["XP",7]
    AsahinoXP = ["XP",8]
    CenmenteryXP = ["XP",9]
    SRGEXPOXP = ["XP",10]
    XixianSouthXP = ["XP",11]
    XixianXP = ["XP",12]
    XixianWestXP = ["XP",13]
    GongjiataiXP = ["XP",14]
    BamaojingXP = ["XP",15]
    ShanmaojuIslandXP = ["XP",16]
    XinquanNanshanXP = ["XP",17]
    
class LineXPZ:
    """新平城际支线"""
    HLIntlAirportXPZ = ["XPZ",1]
    JiulonghuStreetXPZ = ["XPZ",2]
    SangzhiXPZ = ["XPZ",3]
    SinkholeVillageXPZ = ["XPZ",4]
    FredsBeachXPZ = ["XPZ",5]
    ShuangliNewTownEastXPZ = ["XPZ",6]
    BinhaiWestAveneXPZ = ["XPZ",7]
    HujiHingeXPZ = ["XPZ",8]
    JinjialinXPZ = ["XPZ",9]
    ArkSquareXPZ = ["XPZ",10]
    
class Line1:
    """1号线"""
    Fenggangli1 = ["1",1]
    KaiShekMemorial1 = ["1",2]
    RikakoRoad1 = ["1",3]
    WenlanRoad1 = ["1",4]
    Asahino1 = ["1",5]
    HujiHinge1 = ["1",6]
    TechnologyBuilding1 = ["1",7]
    Jinjialin1 = ["1",8]
    ArkSquare1 = ["1",9]
    SportsCenter1 = ["1",10]

class Line2:
    """2号线"""
    MinghuaRoad2 = ["2",16]
    XiyaSouth2 = ["2",15]
    YunlanRoad2 = ["2",14]
    TechInnovationPark2 = ["2",13]
    HuaxingPort2 = ["2",12]
    APFU2 = ["2",11]
    JunpengRoad2 = ["2",10]
    TangpuRoad2 = ["2",9]
    ArkSquare2 = ["2",8]
    Mingguang2 = ["2",7]
    AnpingLibrary2 = ["2",6]
    PingxiBambooForest2 = ["2",5]
    CheckerboardGeopark2 = ["2",4]
    WuchaFlyover2 = ["2",3]
    FuanRoad2 = ["2",2]
    MedicalCollege2 = ["2",1]
    
class Line4:
    """4号线"""
    APFU4 = ["4",1]
    JiefangSquare4 = ["4",2]
    FisheryCollege4 = ["4",3]
    AnpingAcientCity4 = ["4",4]
    Jinjialin4 = ["4",5]
    AirportRunwaySite4 = ["4",6]
    Fulok4 = ["4",7]
    CoachTerminal4 = ["4",8]
    Yuewanglou4 = ["4",9]
    RikakoRoad4 = ["4",10]
    SRGEXPO4 = ["4",11]
    TaichiIsland4 = ["4",12]
    ZhouyuEastRoad4 = ["4",13]
    Xiagang4 = ["4",14]
    
class Line6:
    """6号线"""
    Liufang6 = ["6",1]
    CBCZ6 = ["6",2]
    PakShekKok6 = ["6",3]
    AnpingSciencePark6 = ["6",4]
    FoutrhKangdingRoad6 = ["6",5]
    Gongxingdao6 = ["6",6]
    CangshanRoad6 = ["6",7]
    ErhaiRoad6 = ["6",8]
    MarbleArch6 = ["6",9]
    SportsCenter6 = ["6",10]
    TangpuRoad6 = ["6",11]
    FisheryCollege6 = ["6",12]
    HaitangPark6 = ["6",13]
    Jiuchongtian6 = ["6",14]
    
class LineS5:
    """S5号线"""
    JiulonghuStreetS5 = ["S5",1]
    YansuiS5 = ["S5",2]
    HuangxingS5 = ["S5",3]
    JizhouS5 = ["S5",4]
    BaishaLakeS5 = ["S5",5]
    XiyaNorthS5 = ["S5",6]
    APFUS5 = ["S5",7]
    MingguangS5 = ["S5",8]
    WuchaFlyoverS5 = ["S5",9]
    
class APMXR:
    """郗县捷运红线（环线）"""
    ZhouyuEastRoadXR = ["XR",6,24]
    XixianAdminCenterXR = ["XR",7,23]
    CrowdedForestXR = ["XR",8,22]
    LakeviewMansionXR = ["XR",9,21]
    SnowhillTouristCenterXR = ["XR",10,20]
    MingquanWestRoadXR = ["XR",11,19]
    LiangkeshuXR = ["XR",12,18]
    DeshengGateParkXR = ["XR",1,17]
    TongyiPortXR = ["XR",2,16]
    BaihuatanXR = ["XR",3,15]
    XixianSouthXR = ["XR",4,14]
    FiveKilometersXR = ["XR",5,13]
    
class APMXG:
    """郗县捷运绿线"""
    LotusPondXG = ["XG",1]
    XixianWestXG = ["XG",2]
    BerlinXG = ["XG",3]
    CrowdedForestXG = ["XG",4]
    XixianAdminCenterXG = ["XG",5]
    ZhouyuEastRoadXG = ["XG",6]
    FiveKilometersXG = ["XG",7]
    XixianSouthXG = ["XG",8]
    ManshuiqiaoVillageXG = ["XG",9]
    
class LineHL1:
    """互利1号线"""
    HarmonyNewPortHL1 = ["HL1",1]
    HaizhiyunHL1 = ["HL1",2]
    SubCenterHL1 = ["HL1",3]
    HLNHL1 = ["HL1",4]
    XinghuHL1 = ["HL1",5]
    HarmonySquareHL1 = ["HL1",6]
    QihaiVillageHL1 = ["HL1",7]
    HongweiLanshanHL1 = ["HL1",8]
    FuanSouthHL1 = ["HL1",9]
    HLEHL1 = ["HL1",10]
    
class LineHL2:
    """互利2号线"""
    ZumiaoTempleHL2 = ["HL2",1]
    CostaHL2 = ["HL2",2]
    HuaxiangshanHL2 = ["HL2",3]
    XinghuHL2 = ["HL2",4]
    
class LineHL5:
    """互利5号线"""
    DongfangRoadHL5 = ["HL5",1]
    HongmeiRoadHL5 = ["HL5",2]
    BinhaiJiayuanHL5 = ["HL5",3]
    
class LineHL8:
    """互利8号线"""
    UnderwaterTempleHL8 = ["HL8",1]
    XiaoximenHL8 = ["HL8",2]
    ExpoCenterHL8 = ["HL8",3]
    XinghuHL8 = ["HL8",4]
    HongqiEastRoadHL8 = ["HL8",5]
    LihuaRoadHL8 = ["HL8",6]
    FuluMiddleSchoolHL8 = ["HL8",7]
    FuluYiteVillageHL8 = ["HL8",8]
    
class LineHL16:
    """互利16号线"""
    HLIntlAirportHL16 = ["HL16",1]
    JinwuNorthHL16 = ["HL16",2]
    HonggudiHL16 = ["HL16",3]
    AgricultureAcademyHL16 = ["HL16",4]
    DongfangRoadHL16 = ["HL16",5]
    GaotianyuanHL16 = ["HL16",6]
    GubeiHL16 = ["HL16",7]
    CostaHL16 = ["HL16",8]
    HaixinHL16 = ["HL16",9]
    HLNHL16 = ["HL16",10]
    
class LineHL17:
    """互利17号线"""
    XuanshuHL17 = ["HL17",1]
    SangyuanNorthHL17 = ["HL17",2]
    WanyanRiverHL17 = ["HL17",3]
    RailwayResearchCenterHL17 = ["HL17",4]
    SYIntlAiportHL17 = ["HL17",5]
    XinglinWestHL17 = ["HL17",6]
    ChangqingRoadHL17 = ["HL17",7]
    KaishanHL17 = ["HL17",8]
    CinnamonRoadHL17 = ["HL17",9]
    HLIntlAirportHL17 = ["HL17",10]
    YongningHL17 = ["HL17",11]
    YansuiHL17 = ["HL17",12]
    
class LineHL20:
    """互利20号线 普通车"""
    HLSHL20 = ["HL20",1]
    HarmonySouthSideHL20 = ["HL20",2]
    QinglingHL20 = ["HL20",3]
    LauraCreeksideHL20 = ["HL20",4]
    LinglengEstuaryHL20 = ["HL20",5]
    DaokaibiHL20 = ["HL20",6]
    TunyuShoreHL20 = ["HL20",7]
    HuangxingHL20 = ["HL20",8]
    
class LineHL20S:
    """互利20号线 商务座"""
    HLSHL20S = ["HL20SW",1]
    HuangxingHL20S = ["HL20SW",2]
    JizhouHL20S = ["HL20SW",3]
    BaishaLakeHL20S = ["HL20SW",4]
    XiyaNorthHL20S = ["HL20SW",5]
    APFUHL20S = ["HL20SW",6]
    MingguangHL20S = ["HL20SW",7]
    WuchaFlyoverHL20S = ["HL20SW",8]
    
class LineHLS3:
    """互利S3号线"""
    HLEHLS3 = ["HLS3",1]
    FuanHLS3 = ["HLS3",2]
    FuanMountainHLS3 = ["HLS3",3]
    FuluYiteVillageHLS3 = ["HLS3",4]
    QihaiVillageHLS3 = ["HLS3",5]
    UnderwaterTempleHLS3 = ["HLS3",6]
    JinshanHLS3 = ["HLS3",7]
    BinhaiJiayuanHLS3 = ["HLS3",8]
    
class Station:
    """站点"""
    MinghuaRoad = [Line2.MinghuaRoad2,"明华路"]
    XiyaSouth = [Line2.XiyaSouth2,"犀崖南"]
    YunlanRoad = [Line2.YunlanRoad2,"云岚路"]
    TechInnovationPark = [Line2.TechInnovationPark2,"科创园"]
    HuaxingPort = [Line2.HuaxingPort2,"华兴湾"]
    APFU = [Line2.APFU2,Line4.APFU4,LineS5.APFUS5,LineHL20S.APFUHL20S,"安平财大"]
    JunpengRoad = [Line2.JunpengRoad2,"俊鹏路"]
    TangpuRoad = [Line2.TangpuRoad2,Line6.TangpuRoad6,"塘埔路"]
    ArkSquare = [Line1.ArkSquare1,Line2.ArkSquare2,LineXPZ.ArkSquareXPZ,"方舟广场"]
    Dongsheng = [Line2.Mingguang2,LineS5.MingguangS5,LineHL20S.MingguangHL20S,"明光"]
    AnpingLibrary = [Line2.AnpingLibrary2,"市图书馆"]
    PingxiBambooForest = [Line2.PingxiBambooForest2,"平溪竹海"]
    CheckerboardGeopark = [Line2.CheckerboardGeopark2,"格仔公园"]
    WuchaFlyover = [Line2.WuchaFlyover2,LineS5.WuchaFlyoverS5,LineHL20S.WuchaFlyoverHL20S,"五岔路口"]
    FuanRoad = [Line2.FuanRoad2,"福安路"]
    MedicalCollege = [Line2.MedicalCollege2,"市医学院"]
    JiulonghuStreet = [LineXP.JiulonghuStreetXP,LineXPZ.JiulonghuStreetXPZ,LineS5.JiulonghuStreetS5,"九龙湖街"]
    Yansui = [LineS5.YansuiS5,LineHL17.YansuiHL17,"芫荽"]
    Huangxing = [LineS5.HuangxingS5,LineHL20.HuangxingHL20,LineHL20S.HuangxingHL20S,"黄兴"]
    Jizhou = [LineS5.JizhouS5,LineHL20S.JizhouHL20S,"济舟"]
    BaishaLake = [LineS5.BaishaLakeS5,LineHL20S.BaishaLakeHL20S,"白沙湖"]
    XiyaNorth = [LineS5.XiyaNorthS5,LineHL20S.XiyaNorthHL20S,"犀崖北"]
    HLS = [LineHL20.HLSHL20,LineHL20S.HLSHL20S,"互利南站"]
    HarmonySouthSide = [LineHL20.HarmonySouthSideHL20,"凛冰南界"]
    Qingling = [LineHL20.QinglingHL20,"清灵"]
    LauraCreekside = [LineHL20.LauraCreeksideHL20,"劳拉溪畔"]
    LinglengEstuary = [LineHL20.LinglengEstuaryHL20,"泠棱江口"]
    Daokaibi = [LineHL20.DaokaibiHL20,"道开壁"]
    TunyuShore = [LineHL20.TunyuShoreHL20,"豚雨石岸"]
    Xuanshu = [LineHL17.XuanshuHL17,"悬树"]
    SangyuanNorth = [LineHL17.SangyuanNorthHL17,"桑园北"]
    WanyanRiver = [LineHL17.WanyanRiverHL17,"蜿蜒河"]
    RailwayResearchCenter = [LineHL17.RailwayResearchCenterHL17,"铁研中心"]
    SYIntlAiport = [LineHL17.SYIntlAiportHL17,"桑园国际机场"]
    XinglinWest = [LineHL17.XinglinWestHL17,"杏林西"]
    ChangqingRoad = [LineHL17.ChangqingRoadHL17,"常青路"]
    Kaishan = [LineHL17.KaishanHL17,"开山"]
    CinnamonRoad = [LineHL17.CinnamonRoadHL17,"桂香路"]
    HLIntlAirport = [LineXP.HLIntlAirportXP,LineXPZ.HLIntlAirportXPZ,LineHL16.HLIntlAirportHL16,LineHL17.HLIntlAirportHL17,"黄龙国际机场"]
    Yongning = [LineHL17.YongningHL17,"永宁"]
    Sangzhi = [LineXP.SangzhiXP,LineXPZ.SangzhiXPZ,"桑植"]
    SinkholeVillage = [LineXP.SinkholeVillageXP,LineXPZ.SinkholeVillageXPZ,"天坑村"]
    FredsBeach = [LineXP.FredsBeachXP,LineXPZ.FredsBeachXPZ,"弗雷德沙滩"]
    ShuangliNewTownEast = [LineXP.ShuangliNewTownEastXP,LineXPZ.ShuangliNewTownEastXPZ,"双鲤新城东"]
    BinhaiWestAvene = [LineXP.BinhaiWestAveneXP,LineXPZ.BinhaiWestAveneXPZ,"滨海西大道"]
    HujiHinge = [LineXPZ.HujiHingeXPZ,Line1.HujiHinge1,"湖际枢纽"]
    Jinjialin = [LineXPZ.JinjialinXPZ,Line1.Jinjialin1,Line4.Jinjialin4,"金家林"]
    Asahino_Fulok = [LineXP.AsahinoXP,Line1.Asahino1,Line4.Fulok4,"金花/富乐"]
    Cenmentery = [LineXP.CenmenteryXP,"烈士陵园"]
    SRGEXPO = [LineXP.SRGEXPOXP,Line4.SRGEXPO4,"银江大会展中心"]
    XixianSouth = [LineXP.XixianSouthXP,APMXR.XixianSouthXR,APMXG.XixianSouthXG,"郗县南站"]
    Xixian_Xiagang = [LineXP.XixianXP,Line4.Xiagang4,"郗县站/下港"]
    XixianWest = [LineXP.XixianWestXP,APMXG.XixianWestXG,"郗县西站"]
    Gongjiatai = [LineXP.GongjiataiXP,"贡家台"]
    Bamaojing = [LineXP.BamaojingXP,"八毛井"]
    ShanmaojuIsland = [LineXP.ShanmaojuIslandXP,"山毛榉岛"]
    XinquanNanshan = [LineXP.XinquanNanshanXP,"新权南山"]
    Fenggangli = [Line1.Fenggangli1,"凤岗里"]
    KaiShekMemorial = [Line1.KaiShekMemorial1,"蒋公庙"]
    RikakoRoad = [Line1.RikakoRoad1,Line4.RikakoRoad4,"仙梨路"]
    WenlanRoad = [Line1.WenlanRoad1,"文澜路"]
    TechnologyBuilding = [Line1.TechnologyBuilding1,"科技大楼"]
    SportsCenter = [Line1.SportsCenter1,Line6.SportsCenter6,"体育中心"]
    JiefangSquare = [Line4.JiefangSquare4,"解放广场"]
    FisheryCollege = [Line4.FisheryCollege4,Line6.FisheryCollege6,"水产学院"]
    AnpingAcientCity = [Line4.AnpingAcientCity4,"安平古城"]
    AirportRunwaySite = [Line4.AirportRunwaySite4,"机场跑道旧址"]
    CoachTerminal = [Line4.CoachTerminal4,"汽车总站"]
    Yuewanglou = [Line4.Yuewanglou4,"越王楼"]
    TaichiIsland = [Line4.TaichiIsland4,"太极岛"]
    ZhouyuEastRoad = [Line4.ZhouyuEastRoad4,APMXR.ZhouyuEastRoadXR,APMXG.ZhouyuEastRoadXG,"周瑜东路"]
    XixianAdminCenter = [APMXR.XixianAdminCenterXR,APMXG.XixianAdminCenterXG,"县行政服务中心"]
    CrowdedForest = [APMXR.CrowdedForestXR,APMXG.CrowdedForestXG,"薮渊之林"]
    LakeviewMansion = [APMXR.LakeviewMansionXR,"滨湖居"]
    SnowhillTouristCenter = [APMXR.SnowhillTouristCenterXR,"雪山城市客厅"]
    MingquanWestRoad = [APMXR.MingquanWestRoadXR,"民权西路"]
    Liangkeshu = [APMXR.LiangkeshuXR,"两棵树"]
    DeshengGatePark = [APMXR.DeshengGateParkXR,"德胜门遗址公园"]
    TongyiPort = [APMXR.TongyiPortXR,"同益码头"]
    Baihuatan = [APMXR.BaihuatanXR,"百花潭"]
    FiveKilometers = [APMXR.FiveKilometersXR,APMXG.FiveKilometersXG,"五公里"]
    LotusPond = [APMXG.LotusPondXG,"荷花池头"]
    Berlin = [APMXG.BerlinXG,"柏林"]
    ManshuiqiaoVillage = [APMXG.ManshuiqiaoVillageXG,"漫水桥村"]
    JinwuNorth = [LineHL16.JinwuNorthHL16,"进武北"]
    Honggudi = [LineHL16.HonggudiHL16,"红谷地"]
    AgricultureAcademy = [LineHL16.AgricultureAcademyHL16,"省农科院"]
    DongfangRoad = [LineHL5.DongfangRoadHL5,LineHL16.DongfangRoadHL16,"东方路"]
    Gaotianyuan = [LineHL16.GaotianyuanHL16,"高天原"]
    Gubei = [LineHL16.GubeiHL16,"古北"]
    Haixin = [LineHL16.HaixinHL16,"塰欣"]
    HLN = [LineHL1.HLNHL1,LineHL16.HLNHL16,"互利北站"]
    HarmonyNewPort = [LineHL1.HarmonyNewPortHL1,"互利新港"]
    Haizhiyun = [LineHL1.HaizhiyunHL1,"海之韵"]
    SubCenter = [LineHL1.SubCenterHL1,"副中心"]
    Xinghu = [LineHL1.XinghuHL1,LineHL2.XinghuHL2,LineHL8.XinghuHL8,"星湖"]
    HarmonySquare = [LineHL1.HarmonySquareHL1,"互利广场"]
    QihaiVillage = [LineHL1.QihaiVillageHL1,LineHLS3.QihaiVillageHLS3,"七海村"]
    HongweiLanshan = [LineHL1.HongweiLanshanHL1,"鸿玮澜山"]
    FuanSouth = [LineHL1.FuanSouthHL1,"阜安南"]
    HLE = [LineHL1.HLEHL1,LineHLS3.HLEHLS3,"互利东站"]
    ZumiaoTemple = [LineHL2.ZumiaoTempleHL2,"祖庙"]
    Costa = [LineHL2.CostaHL2,LineHL16.CostaHL16,"海角"]
    Huaxiangshan = [LineHL2.HuaxiangshanHL2,"花响山"]
    HongmeiRoad = [LineHL5.HongmeiRoadHL5,"红梅路"]
    BinhaiJiayuan = [LineHL5.BinhaiJiayuanHL5,LineHLS3.BinhaiJiayuanHLS3,"滨海家园"]
    UnderwaterTemple = [LineHL8.UnderwaterTempleHL8,LineHLS3.UnderwaterTempleHLS3,"海底神殿"]
    Xiaoximen = [LineHL8.XiaoximenHL8,"小西门"]
    ExpoCenter = [LineHL8.ExpoCenterHL8,"会展中心"]
    HongqiEastRoad = [LineHL8.HongqiEastRoadHL8,"红旗东路"]
    LihuaRoad = [LineHL8.LihuaRoadHL8,"丽华路"]
    FuluMiddleSchool = [LineHL8.FuluMiddleSchoolHL8,"弗卢中学"]
    FuluYiteVillage = [LineHL8.FuluYiteVillageHL8,LineHLS3.FuluYiteVillageHLS3,"弗卢伊特村"]
    Fuan = [LineHLS3.FuanHLS3,"阜安"]
    FuanMountain = [LineHLS3.FuanMountainHLS3,"阜安山"]
    Jinshan = [LineHLS3.JinshanHLS3,"金山"]
    Liufang = [Line6.Liufang6,"流芳"]
    CBCZ = [Line6.CBCZ6,"跨境合作区"]
    PakShekKok = [Line6.PakShekKok6,"白石角"]
    AnpingSciencePark = [Line6.AnpingSciencePark6,"安平科学园"]
    FoutrhKangdingRoad = [Line6.FoutrhKangdingRoad6,"康定四路"]
    Gongxingdao = [Line6.Gongxingdao6,"公行道"]
    CangshanRoad = [Line6.CangshanRoad6,"苍山路"]
    ErhaiRoad = [Line6.ErhaiRoad6,"洱海路"]
    MarbleArch = [Line6.MarbleArch6,"凯旋门"]
    HaitangPark = [Line6.HaitangPark6,"海棠公园"]
    Jiuchongtian = [Line6.Jiuchongtian6,"九重天"]