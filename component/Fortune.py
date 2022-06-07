import re
from typing import List
from discord import Client, Embed
import random 
from . import Component

channel_mention_re = re.compile("<#(\d+)>")

previous_players = {}

sentences = [
    "虫を踏みそうです。",
    "車に引かれそうです。",
    "運命の人と出会うでしょう。",
    "家族から電話がかかってくるでしょう。"
    "蚊に刺されるでしょう。",
    "パソコンの調子が悪くなるでしょう。",
    "体の調子が悪くなるでしょう。",
    "お腹をこわすでしょう。",
    "足をくじくでしょう。",
    "手をけがしてしまうでしょう。",
    "悪い夢を見るでしょう。",
    "良い夢を見るでしょう。",
    "スケベな夢を見るでしょう。",
    "特になにもなさそうです。",
    "具体的にはわかりませんが、なにかがあります。",
    "悩みが解決するでしょう。",
    "背中の手が届かないところが痒くなるでしょう。",
    "指の間が痒くなるでしょう。",
    "目が痒くなるでしょう。",
    "爪が割れてしまうおそれあり。",
    "知らないおじさんとぶつかります。",
    "知らないおじさんと喧嘩になります。",
    "知らないおじさんと仲良くなります。",
    "ヤンキーとぶつかります。",
    "ヤンキーと喧嘩になります。",
    "ヤンキーと仲良くなります。",
    "ギャルとぶつかります。",
    "ギャルと喧嘩になります。",
    "ギャルと仲良くなります。",
    "財布をなくすでしょう。",
    "家の鍵をなくすでしょう。",
    "スマホをなくすでしょう。",
    "大事な物をなくすでしょう。",
    "新しい友だちができるでしょう。",
    "友だちが減るでしょう。",
    "Youtubeが重くなるでしょう。",
    "Wifiが重くなるでしょう。",
    "Twitterでバズるでしょう。",
    "ゴミ箱を倒すでしょう。",
    "爪の間にゴミが挟まるでしょう。",
    "髪にゴミが絡まるでしょう。",
    "ご飯をこぼすでしょう。",
    "飲み物をこぼすでしょう。",
    "お菓子をこぼすでしょう。",
    "イライラすることがあるでしょう。",
    "楽しいことがあるでしょう。",
    "悲しいことがあるでしょう。",
    "自分のことを棚にあげてしまうでしょう。"
    "誰かにブチギレてしまうでしょう。",
    "なにかに全力で取り組めるでしょう。",
    "なにかにちょっと取り組めるでしょう。",
    "なにかに取り組む気力がなくなるでしょう。",
    "他人に厳しくなってしまうでしょう。",
    "自分を甘やかしてしまうでしょう。",
    "美味しいパン屋を見つけるでしょう。",
    "美味しいラーメン屋を見つけるでしょう。",
    "新しい趣味を見つけるでしょう。",
    "知らない人から電話がかかってくるでしょう。",
    "全力で逃げろ。",
    "末代まで呪われるでしょう。",
    "お金を拾うでしょう。",
    "一万円を拾うでしょう。",
    "誤字をしてしまいそうです。",
    "家に虫が入ってくるでしょう。",
    "家電が壊れるでしょう。",
]

rare_sentences = [
    "着席時コップに水垢が付いていたのを見て大きな声を出したら店主さんからの誠意でチャーシューをサービスしてもらえるでしょう。",
    "あぁ^～心がぴょんぴょんするでしょう。"
    "ぺこーらいつもありがとう！ 最近ぺこーらへ感謝するのが日課になりつつあるでしょう。",
    "愛のままにわがままに僕は君だけを傷つけないでしょう。",
    "女々しくて女々しくて女々しくて辛いでしょう。",
    "うんこを踏みそうです。",
]

lucks = ["大吉", "中吉", "吉", "小吉", "末吉", "凶", "大凶"]
positions = ["トップ", "ジャングル", "ミッド", "サポート", "ADC"]
champions = ["アーゴット", "アーリ", "アイバーン", "アカリ", "アクシャン", "アジール", "アッシュ", "アニー", "アニビア", "アフェリオス", "アムム", "アリスター", "イブリン", "イラオイ", "イレリア", "ウーコン", "ウディア", "エイトロックス", "エコー", "エズリアル", "エリス", "オーン", "オラフ", "オリアナ", "オレリオン・ソル", "カーサス", "カ＝ジックス", "カイ＝サ", "カサディン", "カシオペア", "カタリナ", "カミール", "カリスタ", "カルマ", "ガリオ", "ガレン", "ガングプランク", "キヤナ", "キンドレッド", "クイン", "クレッド", "グウェン", "グラガス", "グレイブス", "ケイトリン", "ケイル", "ケイン", "ケネン", "コーキ", "コグ＝マウ", "サイオン", "サイラス", "サミーラ", "ザイラ", "ザック", "ザヤ", "シェン", "シャコ", "シン・ジャオ", "シンジド", "シンドラ", "シヴァーナ", "シヴィア", "ジェイス", "ジグス", "ジャーヴァンIV", "ジャックス", "ジャンナ", "ジリアン", "ジン", "ジンクス", "スウェイン", "スカーナー", "スレッシュ", "セジュアニ", "セト", "セナ", "セラフィーン", "ゼド", "ゼラス", "ゼリ", "ソナ", "ソラカ", "ゾーイ", "タム・ケンチ", "タリック", "タリヤ", "タロン", "ダイアナ", "ダリウス", "チョ＝ガス", "ツイステッド・フェイト", "ティーモ", "トゥイッチ", "トランドル", "トリスターナ", "トリンダメア", "ドクター・ムンド", "ドレイヴン", "ナー", "ナサス", "ナミ", "ニーコ", "ニダリー", "ヌヌ＆ウィルンプ", "ノーチラス", "ノクターン", "ハイマーディンガー", "バード", "パイク", "パンテオン", "ビクター", "フィオラ", "フィズ", "フィドルスティックス", "ブラウム", "ブラッドミア", "ブランド", "ブリッツクランク", "ヘカリム", "ベイガー", "ボリベア", "ポッピー", "マオカイ", "マスター・イー", "マルザハール", "マルファイト", "ミス・フォーチュン", "モルガナ", "モルデカイザー", "ヤスオ", "ユーミ", "ヨネ", "ヨリック", "ライズ", "ラカン", "ラックス", "ラムス", "ランブル", "リー・シン", "リサンドラ", "リリア", "リヴェン", "ルシアン", "ルブラン", "ルル", "レオナ", "レク＝サイ", "レナータ・グラスク", "レネクトン", "レル", "レンガー", "ワーウィック", "ヴァイ", "ヴァルス", "ヴィエゴ", "ヴェイン", "ヴェックス", "ヴェル＝コズ"]
agents = ["レイナ", "オーメン", "スカイ", "ヨル", "チェンバー", "ネオン", "レイズ", "ヴァイパー", "ブリーチ", "アストラ", "KAY/O", "サイファー", "キルジョイ", "フェイド"]

colors = [{"code":0xfef4f4,"name":"桜色"},{"code":0x96514d,"name":"小豆色"},{"code":0xe6b422,"name":"黄金"},{"code":0x006e54,"name":"萌葱色"},{"code":0x895b8a,"name":"古代紫"},{"code":0xfdeff2,"name":"薄桜"},{"code":0x8d6449,"name":"枯茶"},{"code":0xd9a62e,"name":"櫨染"},{"code":0x00a381,"name":"花緑青"},{"code":0x824880,"name":"茄子紺"},{"code":0xe9dfe5,"name":"桜鼠"},{"code":0xdeb068,"name":"飴色"},{"code":0xd3a243,"name":"黄朽葉色"},{"code":0x38b48b,"name":"翡翠色"},{"code":0x915c8b,"name":"二藍"},{"code":0xe4d2d8,"name":"鴇鼠"},{"code":0xbf794e,"name":"駱駝色"},{"code":0xc89932,"name":"山吹茶"},{"code":0x00a497,"name":"青緑"},{"code":0x9d5b8b,"name":"京紫"},{"code":0xf6bfbc,"name":"虹色"},{"code":0xbc763c,"name":"土色"},{"code":0xd0af4c,"name":"芥子色"},{"code":0x80aba9,"name":"水浅葱"},{"code":0x7a4171,"name":"蒲葡"},{"code":0xf5b1aa,"name":"珊瑚色"},{"code":0xb98c46,"name":"黄唐茶"},{"code":0x8b968d,"name":"豆がら茶"},{"code":0x5c9291,"name":"錆浅葱"},{"code":0xbc64a4,"name":"若紫"},{"code":0xf5b199,"name":"一斤染"},{"code":0xb79b5b,"name":"桑染"},{"code":0x6e7955,"name":"麹塵"},{"code":0x478384,"name":"青碧"},{"code":0xb44c97,"name":"紅紫"},{"code":0xefab93,"name":"宍色"},{"code":0xb77b57,"name":"櫨色"},{"code":0x767c6b,"name":"山鳩色"},{"code":0x43676b,"name":"御召茶"},{"code":0xaa4c8f,"name":"梅紫"},{"code":0xf2a0a1,"name":"紅梅色"},{"code":0xb68d4c,"name":"黄橡"},{"code":0x888e7e,"name":"利休鼠"},{"code":0x80989b,"name":"湊鼠"},{"code":0xcc7eb1,"name":"菖蒲色"},{"code":0xf0908d,"name":"薄紅"},{"code":0xad7d4c,"name":"丁字染"},{"code":0x5a544b,"name":"海松茶"},{"code":0x2c4f54,"name":"高麗納戸"},{"code":0xcca6bf,"name":"紅藤色"},{"code":0xee827c,"name":"甚三紅"},{"code":0xad7d4c,"name":"香染"},{"code":0x56564b,"name":"藍海松茶"},{"code":0x1f3134,"name":"百入茶"},{"code":0xc4a3bf,"name":"浅紫"},{"code":0xf09199,"name":"桃色"},{"code":0xae7c4f,"name":"枇杷茶"},{"code":0x555647,"name":"藍媚茶"},{"code":0x47585c,"name":"錆鼠"},{"code":0xe7e7eb,"name":"紫水晶"},{"code":0xf4b3c2,"name":"鴇色"},{"code":0xad7e4e,"name":"芝翫茶"},{"code":0x494a41,"name":"千歳茶"},{"code":0x485859,"name":"錆鉄御納戸"},{"code":0xdcd6d9,"name":"薄梅鼠"},{"code":0xeebbcb,"name":"撫子色"},{"code":0xae7c58,"name":"焦香"},{"code":0x6b6f59,"name":"岩井茶"},{"code":0x6c848d,"name":"藍鼠"},{"code":0xd3cfd9,"name":"暁鼠"},{"code":0xe8d3c7,"name":"灰梅"},{"code":0xa86f4c,"name":"胡桃色"},{"code":0x474b42,"name":"仙斎茶"},{"code":0x53727d,"name":"錆御納戸"},{"code":0xd3ccd6,"name":"牡丹鼠"},{"code":0xe8d3d1,"name":"灰桜"},{"code":0x946243,"name":"渋紙色"},{"code":0x333631,"name":"黒緑"},{"code":0x5b7e91,"name":"舛花色"},{"code":0xc8c2c6,"name":"霞色"},{"code":0xe6cde3,"name":"淡紅藤"},{"code":0x917347,"name":"朽葉色"},{"code":0x5b6356,"name":"柳煤竹"},{"code":0x426579,"name":"熨斗目花色"},{"code":0xa6a5c4,"name":"藤鼠"},{"code":0xe5abbe,"name":"石竹色"},{"code":0x956f29,"name":"桑茶"},{"code":0x726250,"name":"樺茶色"},{"code":0x4c6473,"name":"御召御納戸"},{"code":0xa69abd,"name":"半色"},{"code":0xe597b2,"name":"薄紅梅"},{"code":0x8c7042,"name":"路考茶"},{"code":0x9d896c,"name":"空五倍子色"},{"code":0x455765,"name":"鉄御納戸"},{"code":0xa89dac,"name":"薄色"},{"code":0xe198b4,"name":"桃花色"},{"code":0x7b6c3e,"name":"国防色"},{"code":0x94846a,"name":"生壁色"},{"code":0x44617b,"name":"紺鼠"},{"code":0x9790a4,"name":"薄鼠"},{"code":0xe4ab9b,"name":"水柿"},{"code":0xd8a373,"name":"伽羅色"},{"code":0x897858,"name":"肥後煤竹"},{"code":0x393f4c,"name":"藍鉄"},{"code":0x9e8b8e,"name":"鳩羽鼠"},{"code":0xe09e87,"name":"ときがら茶"},{"code":0xcd8c5c,"name":"江戸茶"},{"code":0x716246,"name":"媚茶"},{"code":0x393e4f,"name":"青褐"},{"code":0x95859c,"name":"鳩羽色"},{"code":0xd69090,"name":"退紅"},{"code":0xcd5e3c,"name":"樺色"},{"code":0xcbb994,"name":"白橡"},{"code":0x203744,"name":"褐返"},{"code":0x95949a,"name":"桔梗鼠"},{"code":0xd4acad,"name":"薄柿"},{"code":0xcb8347,"name":"紅鬱金"},{"code":0xd6c6af,"name":"亜麻色"},{"code":0x4d4c61,"name":"褐色"},{"code":0x71686c,"name":"紫鼠"},{"code":0xc97586,"name":"長春色"},{"code":0xc37854,"name":"土器色"},{"code":0xbfa46f,"name":"榛色"},{"code":0xeaf4fc,"name":"月白"},{"code":0x705b67,"name":"葡萄鼠"},{"code":0xc099a0,"name":"梅鼠"},{"code":0xc38743,"name":"狐色"},{"code":0x9e9478,"name":"灰汁色"},{"code":0xeaedf7,"name":"白菫色"},{"code":0x634950,"name":"濃色"},{"code":0xb88884,"name":"鴇浅葱"},{"code":0xc39143,"name":"黄土色"},{"code":0xa59564,"name":"利休茶"},{"code":0xe8ecef,"name":"白花色"},{"code":0x5f414b,"name":"紫鳶"},{"code":0xb48a76,"name":"梅染"},{"code":0xbf783a,"name":"琥珀色"},{"code":0x715c1f,"name":"鶯茶"},{"code":0xebf6f7,"name":"藍白"},{"code":0x4f455c,"name":"濃鼠"},{"code":0xa86965,"name":"蘇芳香"},{"code":0xbb5535,"name":"赤茶"},{"code":0xc7b370,"name":"木蘭色"},{"code":0xc1e4e9,"name":"白藍"},{"code":0x5a5359,"name":"藤煤竹"},{"code":0xa25768,"name":"浅蘇芳"},{"code":0xbb5520,"name":"代赭"},{"code":0xdcd3b2,"name":"砂色"},{"code":0xbce2e8,"name":"水色"},{"code":0x594255,"name":"滅紫"},{"code":0xec6d71,"name":"真朱"},{"code":0xb55233,"name":"煉瓦色"},{"code":0xa19361,"name":"油色"},{"code":0xa2d7dd,"name":"瓶覗"},{"code":0x524748,"name":"紅消鼠"},{"code":0xeb6ea5,"name":"赤紫"},{"code":0xaa4f37,"name":"雀茶"},{"code":0x8f8667,"name":"利休色"},{"code":0xabced8,"name":"秘色色"},{"code":0x513743,"name":"似せ紫"},{"code":0xe95295,"name":"躑躅色"},{"code":0x9f563a,"name":"団十郎茶"},{"code":0x887938,"name":"梅幸茶"},{"code":0xa0d8ef,"name":"空色"},{"code":0xe6eae3,"name":"灰黄緑"},{"code":0xe7609e,"name":"牡丹色"},{"code":0x9f563a,"name":"柿渋色"},{"code":0x6a5d21,"name":"璃寛茶"},{"code":0x89c3eb,"name":"勿忘草色"},{"code":0xd4dcd6,"name":"蕎麦切色"},{"code":0xd0576b,"name":"今様色"},{"code":0x9a493f,"name":"紅鳶"},{"code":0x918754,"name":"黄海松茶"},{"code":0x84a2d4,"name":"青藤色"},{"code":0xd4dcda,"name":"薄雲鼠"},{"code":0xc85179,"name":"中紅"},{"code":0x98623c,"name":"灰茶"},{"code":0xa69425,"name":"菜種油色"},{"code":0x83ccd2,"name":"白群"},{"code":0xd3cbc6,"name":"枯野色"},{"code":0xe9546b,"name":"薔薇色"},{"code":0x965042,"name":"茶色"},{"code":0xada250,"name":"青朽葉"},{"code":0x84b9cb,"name":"浅縹"},{"code":0xc8c2be,"name":"潤色"},{"code":0xe95464,"name":"韓紅"},{"code":0x965036,"name":"檜皮色"},{"code":0x938b4b,"name":"根岸色"},{"code":0x698aab,"name":"薄花色"},{"code":0xb3ada0,"name":"利休白茶"},{"code":0xc85554,"name":"銀朱"},{"code":0x95483f,"name":"鳶色"},{"code":0x8c8861,"name":"鶸茶"},{"code":0x008899,"name":"納戸色"},{"code":0xa99e93,"name":"茶鼠"},{"code":0xc53d43,"name":"赤紅"},{"code":0x954e2a,"name":"柿茶"},{"code":0xa1a46d,"name":"柳茶"},{"code":0x00a3af,"name":"浅葱色"},{"code":0xa58f86,"name":"胡桃染"},{"code":0xe83929,"name":"紅緋"},{"code":0x8f2e14,"name":"弁柄色"},{"code":0x726d40,"name":"海松色"},{"code":0x2a83a2,"name":"花浅葱"},{"code":0x928178,"name":"江戸鼠"},{"code":0xe60033,"name":"赤"},{"code":0x8a3319,"name":"赤錆色"},{"code":0x928c36,"name":"鶯色"},{"code":0x59b9c6,"name":"新橋色"},{"code":0x887f7a,"name":"煤色"},{"code":0xe2041b,"name":"猩々緋"},{"code":0x8a3b00,"name":"褐色"},{"code":0xdccb18,"name":"緑黄色"},{"code":0x2ca9e1,"name":"天色"},{"code":0xb4866b,"name":"丁子茶"},{"code":0xd7003a,"name":"紅"},{"code":0x852e19,"name":"栗梅"},{"code":0xd7cf3a,"name":"鶸色"},{"code":0x38a1db,"name":"露草色"},{"code":0xb28c6e,"name":"柴染"},{"code":0xc9171e,"name":"深緋"},{"code":0x7b4741,"name":"紅檜皮"},{"code":0xc5c56a,"name":"抹茶色"},{"code":0x0095d9,"name":"青"},{"code":0xa16d5d,"name":"宗伝唐茶"},{"code":0xd3381c,"name":"緋色"},{"code":0x773c30,"name":"海老茶"},{"code":0xc3d825,"name":"若草色"},{"code":0x0094c8,"name":"薄藍"},{"code":0x9f6f55,"name":"砺茶"},{"code":0xce5242,"name":"赤丹"},{"code":0x783c1d,"name":"唐茶"},{"code":0xb8d200,"name":"黄緑"},{"code":0x2792c3,"name":"縹色"},{"code":0x8c6450,"name":"煎茶色"},{"code":0xd9333f,"name":"紅赤"},{"code":0x762f07,"name":"栗色"},{"code":0xe0ebaf,"name":"若芽色"},{"code":0x007bbb,"name":"紺碧"},{"code":0x856859,"name":"銀煤竹"},{"code":0xb94047,"name":"臙脂"},{"code":0x752100,"name":"赤銅色"},{"code":0xd8e698,"name":"若菜色"},{"code":0x5383c3,"name":"薄群青"},{"code":0x765c47,"name":"黄枯茶"},{"code":0xba2636,"name":"朱・緋"},{"code":0x6c3524,"name":"錆色"},{"code":0xc7dc68,"name":"若苗色"},{"code":0x5a79ba,"name":"薄花桜"},{"code":0x6f514c,"name":"煤竹色"},{"code":0xb7282e,"name":"茜色"},{"code":0x683f36,"name":"赤褐色"},{"code":0x99ab4e,"name":"青丹"},{"code":0x4c6cb3,"name":"群青色"},{"code":0x6f4b3e,"name":"焦茶"},{"code":0xa73836,"name":"紅海老茶"},{"code":0x664032,"name":"茶褐色"},{"code":0x7b8d42,"name":"草色"},{"code":0x3e62ad,"name":"杜若色"},{"code":0x544a47,"name":"黒橡"},{"code":0x9e3d3f,"name":"蘇芳"},{"code":0x6d3c32,"name":"栗皮茶"},{"code":0x69821b,"name":"苔色"},{"code":0x1e50a2,"name":"瑠璃色"},{"code":0x543f32,"name":"憲法色"},{"code":0xa22041,"name":"真紅"},{"code":0x583822,"name":"黒茶"},{"code":0xaacf53,"name":"萌黄"},{"code":0x507ea4,"name":"薄縹"},{"code":0x554738,"name":"涅色"},{"code":0xa22041,"name":"濃紅"},{"code":0x6c2c2f,"name":"葡萄茶"},{"code":0xb0ca71,"name":"苗色"},{"code":0x19448e,"name":"瑠璃紺"},{"code":0x433d3c,"name":"檳榔子染"},{"code":0xf8f4e6,"name":"象牙色"},{"code":0x640125,"name":"葡萄色"},{"code":0xb9d08b,"name":"若葉色"},{"code":0x164a84,"name":"紺瑠璃"},{"code":0x432f2f,"name":"黒鳶"},{"code":0xede4cd,"name":"練色"},{"code":0xf8b862,"name":"萱草色"},{"code":0x839b5c,"name":"松葉色"},{"code":0x165e83,"name":"藍色"},{"code":0x3f312b,"name":"赤墨"},{"code":0xe9e4d4,"name":"灰白色"},{"code":0xf6ad49,"name":"柑子色"},{"code":0xcee4ae,"name":"夏虫色"},{"code":0x274a78,"name":"青藍"},{"code":0x302833,"name":"黒紅"},{"code":0xebe1a9,"name":"蒸栗色"},{"code":0xf39800,"name":"金茶"},{"code":0x82ae46,"name":"鶸萌黄"},{"code":0x2a4073,"name":"深縹"},{"code":0xffffff,"name":"白"},{"code":0xf2f2b0,"name":"女郎花"},{"code":0xf08300,"name":"蜜柑色"},{"code":0xa8c97f,"name":"柳色"},{"code":0x223a70,"name":"紺色"},{"code":0xfffffc,"name":"胡粉色"},{"code":0xe4dc8a,"name":"枯草色"},{"code":0xec6d51,"name":"鉛丹色"},{"code":0x9ba88d,"name":"青白橡"},{"code":0x192f60,"name":"紺青"},{"code":0xf7fcfe,"name":"卯の花色"},{"code":0xf8e58c,"name":"淡黄"},{"code":0xee7948,"name":"黄丹"},{"code":0xc8d5bb,"name":"柳鼠"},{"code":0x1c305c,"name":"留紺"},{"code":0xf8fbf8,"name":"白磁"},{"code":0xddbb99,"name":"白茶"},{"code":0xed6d3d,"name":"柿色"},{"code":0xc1d8ac,"name":"裏葉柳"},{"code":0x0f2350,"name":"濃藍"},{"code":0xfbfaf5,"name":"生成り色"},{"code":0xd7a98c,"name":"赤白橡"},{"code":0xec6800,"name":"黄赤"},{"code":0xa8bf93,"name":"山葵色"},{"code":0x17184b,"name":"鉄紺"},{"code":0xf3f3f3,"name":"乳白色"},{"code":0xf2c9ac,"name":"洗柿"},{"code":0xec6800,"name":"人参色"},{"code":0x769164,"name":"老竹色"},{"code":0x0d0015,"name":"漆黒"},{"code":0xf3f3f2,"name":"白練"},{"code":0xfff1cf,"name":"鳥の子色"},{"code":0xee7800,"name":"橙色"},{"code":0xd6e9ca,"name":"白緑"},{"code":0xbbc8e6,"name":"淡藤色"},{"code":0xeae5e3,"name":"素色"},{"code":0xfddea5,"name":"蜂蜜色"},{"code":0xeb6238,"name":"照柿"},{"code":0x93ca76,"name":"淡萌黄"},{"code":0xbbbcde,"name":"藤色"},{"code":0xe5e4e6,"name":"白梅鼠"},{"code":0xfce2c4,"name":"肌色"},{"code":0xea5506,"name":"赤橙"},{"code":0x93b881,"name":"柳染"},{"code":0x8491c3,"name":"紅掛空色"},{"code":0xdcdddd,"name":"白鼠"},{"code":0xfde8d0,"name":"薄卵色"},{"code":0xea5506,"name":"金赤"},{"code":0xbadcad,"name":"薄萌葱"},{"code":0x8491c3,"name":"紅碧"},{"code":0xdddcd6,"name":"絹鼠"},{"code":0xf9c89b,"name":"雄黄"},{"code":0xeb6101,"name":"朱色"},{"code":0x97a791,"name":"深川鼠"},{"code":0x4d5aaf,"name":"紺桔梗"},{"code":0xc0c6c9,"name":"灰青"},{"code":0xf7bd8f,"name":"洒落柿"},{"code":0xe49e61,"name":"小麦色"},{"code":0x98d98e,"name":"若緑"},{"code":0x4d5aaf,"name":"花色"},{"code":0xafafb0,"name":"銀鼠"},{"code":0xf6b894,"name":"赤香"},{"code":0xe45e32,"name":"丹色"},{"code":0x88cb7f,"name":"浅緑"},{"code":0x4a488e,"name":"紺藍"},{"code":0xadadad,"name":"薄鈍"},{"code":0xf4dda5,"name":"砥粉色"},{"code":0xe17b34,"name":"黄茶"},{"code":0x69b076,"name":"薄緑"},{"code":0x4d4398,"name":"紅桔梗"},{"code":0xa3a3a2,"name":"薄墨色"},{"code":0xf1bf99,"name":"肉色"},{"code":0xdd7a56,"name":"肉桂色"},{"code":0x6b7b6e,"name":"青鈍"},{"code":0x5654a2,"name":"桔梗色"},{"code":0x9ea1a3,"name":"錫色"},{"code":0xf1bf99,"name":"人色"},{"code":0xdb8449,"name":"赤朽葉色"},{"code":0xbed2c3,"name":"青磁鼠"},{"code":0x706caa,"name":"藤納戸"},{"code":0x9fa0a0,"name":"素鼠"},{"code":0xefcd9a,"name":"丁子色"},{"code":0xd66a35,"name":"黄櫨染"},{"code":0x93b69c,"name":"薄青"},{"code":0x68699b,"name":"紅掛花色"},{"code":0x949495,"name":"鼠色"},{"code":0xefcd9a,"name":"香色"},{"code":0xffd900,"name":"蒲公英色"},{"code":0xa6c8b2,"name":"錆青磁"},{"code":0x867ba9,"name":"紫苑色"},{"code":0x888084,"name":"源氏鼠"},{"code":0xf0cfa0,"name":"薄香"},{"code":0xffd900,"name":"黄色"},{"code":0x47885e,"name":"緑青色"},{"code":0xdbd0e6,"name":"白藤色"},{"code":0x7d7d7d,"name":"灰色"},{"code":0xedd3a1,"name":"浅黄"},{"code":0xffea00,"name":"中黄"},{"code":0x316745,"name":"千歳緑"},{"code":0xa59aca,"name":"藤紫"},{"code":0x7b7c7d,"name":"鉛色"},{"code":0xe0c38c,"name":"枯色"},{"code":0xffec47,"name":"菜の花色"},{"code":0x68be8d,"name":"若竹色"},{"code":0x7058a3,"name":"菫色"},{"code":0x727171,"name":"鈍色"},{"code":0xf3bf88,"name":"淡香"},{"code":0xfef263,"name":"黄檗色"},{"code":0x3eb370,"name":"緑"},{"code":0x674598,"name":"青紫"},{"code":0x595857,"name":"墨"},{"code":0xf7b977,"name":"杏色"},{"code":0xfcd575,"name":"卵色"},{"code":0x007b43,"name":"常磐色"},{"code":0x674196,"name":"菖蒲色"},{"code":0x595455,"name":"丼鼠"},{"code":0xf19072,"name":"東雲色"},{"code":0xfbd26b,"name":"花葉色"},{"code":0xbed3ca,"name":"千草鼠"},{"code":0x9079ad,"name":"竜胆色"},{"code":0x524e4d,"name":"消炭色"},{"code":0xf19072,"name":"曙色"},{"code":0xf5e56b,"name":"刈安色"},{"code":0x92b5a9,"name":"千草色"},{"code":0x745399,"name":"江戸紫"},{"code":0x474a4d,"name":"藍墨茶"},{"code":0xee836f,"name":"珊瑚朱色"},{"code":0xeec362,"name":"玉蜀黍色"},{"code":0x7ebea5,"name":"青磁色"},{"code":0x65318e,"name":"本紫"},{"code":0x383c3c,"name":"羊羹色"},{"code":0xeb9b6f,"name":"深支子"},{"code":0xebd842,"name":"金糸雀色"},{"code":0x7ebeab,"name":"青竹色"},{"code":0x522f60,"name":"葡萄色"},{"code":0x2b2b2b,"name":"蝋色"},{"code":0xe0815e,"name":"纁"},{"code":0xffdb4f,"name":"黄支子色"},{"code":0x028760,"name":"常磐緑"},{"code":0x493759,"name":"深紫"},{"code":0x2b2b2b,"name":"黒"},{"code":0xdf7163,"name":"浅緋"},{"code":0xfbca4d,"name":"支子色"},{"code":0x3b7960,"name":"木賊色"},{"code":0x2e2930,"name":"紫黒"},{"code":0x180614,"name":"烏羽色"},{"code":0xd57c6b,"name":"真赭"},{"code":0xfcc800,"name":"向日葵色"},{"code":0x2f5d50,"name":"天鵞絨"},{"code":0x884898,"name":"紫"},{"code":0x281a14,"name":"鉄黒"},{"code":0xd0826c,"name":"洗朱"},{"code":0xf8b500,"name":"山吹色"},{"code":0x3a5b52,"name":"虫襖"},{"code":0xc0a2c7,"name":"薄葡萄"},{"code":0x000b00,"name":"濡羽色"},{"code":0xca8269,"name":"遠州茶"},{"code":0xfabf14,"name":"鬱金色"},{"code":0x475950,"name":"革色"},{"code":0x460e44,"name":"紫紺"},{"code":0x250d00,"name":"黒檀"},{"code":0xbb5548,"name":"紅樺色"},{"code":0xf7c114,"name":"藤黄"},{"code":0x00552e,"name":"深緑"},{"code":0x74325c,"name":"暗紅色"},{"code":0x241a08,"name":"憲法黒茶"},{"code":0xab6953,"name":"赭"},{"code":0xe6b422,"name":"金色"},{"code":0x005243,"name":"鉄色"},{"code":0x55295b,"name":"桑の実色"},{"code":0x16160e,"name":"暗黒色"}]

class Fortune(Component):
    def __init__(self, client: Client):
        super().__init__("fortune", "占い", client, alias=["ft"], command="")

    async def on_message(self, message, contents):
        color = random.choice(colors)
        luck = random.choice(lucks)
        sentence = random.choice(rare_sentences) if random.random() < 0.005 else random.choice(sentences)
        position = random.choice(positions)
        chanmpion = random.choice(champions)
        agent = random.choice(agents)

        embed = Embed(
            title="占い結果", 
            color=color["code"],
            description=sentence
        )
        embed.add_field(name='運勢', value=luck, inline=True)
        embed.add_field(name='ラッキーカラー', value=color["name"], inline=True)
        embed.add_field(name='ラッキーLoLポジション', value=position, inline=True)
        embed.add_field(name='ラッキーLoLチャンピオン', value=chanmpion, inline=True)
        embed.add_field(name='ラッキーValorantエージェント', value=agent, inline=True)
        await message.channel.send(embed=embed)


        
    def get_help(self):
        return "\n".join([
            "占いをします。valやlolのキャラピックに迷ったときに是非!",
        ])
