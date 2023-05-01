from Assets.DataHandling.FileHandling.Read import Read
from Assets.DataHandling.FileHandling.Write import Write


file = Read("data.json").extract()
result = []
for unit in file["units"]:
    result.append(unit['title'])
Write('','new.json', result).dump()