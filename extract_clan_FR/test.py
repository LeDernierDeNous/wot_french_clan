data = {
    "500075612": {
        "clan_tag": "--C_N",
        "clan_name": "** Cosa ** Nostra **"
    },
    "500156645": {
        "clan_tag": "--HGS",
        "clan_name": "La Horde des Grognards Sauvages"
    }
}

tag_to_test = "--C_N"

if tag_to_test in [d['clan_tag'] for d in data.values()]:
    print(f"{tag_to_test} found in clan tags")
else:
    print(f"{tag_to_test} not found in clan tags")
