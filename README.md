# random-csv

Generate a random CSV file with a schema.

## Features

* Provide a schema with labels specifying generators (see below)
* Can supply filemask to name file (extension is always txt for now)
* Can add datetime stamp to filename (useful for many files)
* Can supply seed for repeated result
* Generators:
1. int = random integer
2. float = random floating point number
3. str = random string
4. ip = random (possibly legal) ip address (IPv4)
5. date = random date and time stamp
6. word = random namealizer word
7. pipewords = one to three pipedelimited random namealizer words
8. level = simulated log entries

Namealizer words generated using the project at
https://github.com/LeonardMH/namealizer

## Usage

Get help with `-h`

Example usage:

```python
python generate_csv.py 20 --filemask=test --addtimestamp --delimiter=, --how-many=1 --seed=42 word pipewords int float str ip date
```

generates

```csv
chickadee,ottoman|footloose,977247483,0.6513659708910177,YGdANpb1kL f,214.72.242.43,15/07/68_09:25
weltgericht,digging|excrutiate,203377916,0.6820982342909993, c30qXjZixkP,146.250.126.67,24/10/85_12:49
xxxi,gaminess,380876437,0.5020217306561476,Jqq5hYHxbMKt,29.197.124.179,25/05/11_16:25
neglectful,cuddlesome|peopled,415526836,0.23133770574488732,YJGCQLuOECQy,161.231.174.173,07/06/55_14:57
watchmen,hectogram|labefy|necromancer,607148586,0.8623465296977945,6Hm6oE Z2w9d,146.160.36.40,09/12/99_13:55
latimeria,reliquary,460558407,0.19096836645710646,VcCXUTBN5ocB,2.231.95.172,20/01/35_07:02
bryozoa,unrecognizable|june|xenogenesis,836531532,0.5428187179732427,96cQflLYpnLi,92.167.5.181,10/12/19_03:35
yellowhammer,torminous|nonconvertible,299789716,0.40869732698619643,LyJqWV MPGg7,74.41.133.223,01/02/59_11:16
treatise,november|adnate|orangeade,456319311,0.4657194531996979,PAPkSsAd6N Y,185.220.64.241,18/02/81_14:36
inpouring,wether|quitter|borax,953039505,0.5847273681773196,aNYkvuANyGln,179.251.188.69,28/06/54_18:06
technique,rheumatic,636848006,0.168197555714116,VLjSEmWy8lDW,69.233.131.107,04/11/54_07:44
xerophytic,zimbabwean|rebelliously,313904427,0.8324568951434123,qaaREX1ODCpz,96.2.13.72,18/12/77_01:38
dishing,cinderella,871583988,0.26115833539409206,3evU0fcP7Kab,116.18.219.188,19/03/38_17:33
woodsman,dulcoration,863731646,0.9963406857537261,Vwg7tv8yEKkl,61.121.10.55,16/06/89_21:56
scotomy,insubstantial|yule,891515188,0.4092186157762434,oBaUCCF0lTum,192.54.134.115,19/04/24_14:29
wifery,faedera|package,722347800,0.4711625604931251,2rxI0wACZP67,78.24.234.200,30/12/81_19:48
invite,budded,238216264,0.22466731661976935,0t2DfEuH4ysk,187.41.208.135,18/02/73_21:28
illaffected,counterbalancing|utilitarianism,679233290,0.8614912793594435,EIBkP jgLADm,155.189.229.182,14/11/64_07:28
falcade,laceration|various,157596702,0.9565387655254016,e1BC3rk9951k,23.196.173.75,09/02/73_17:36
lepisosteus,offal,277563940,0.8148717226958585,5cF 3wuLv5IZ,26.62.27.29,18/08/33_05:11

```
