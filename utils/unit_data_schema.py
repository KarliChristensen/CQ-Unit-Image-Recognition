# unit_data_schema.py

unit_data = {
            "main_values": {
                "unit_name": main_data.get("unit_name"),
                "unit_tier": main_data.get("unit_tier"),
                "unit_max_level": main_data.get("max_level"),
                "unit_icon_path": main_data.get("icon_path"),
                "unit_type": main_data.get("unit_type"),
            "attributes": {
                "basic_attributes": {
                    "health": basic_data.get("health"),
                    "strength": basic_data.get("strength"),
                    "leadership": basic_data.get("leadership"),
                    "speed": basic_data.get("spped"),
                    "range": basic_data.get("range"),
                    "ammo": basic_data.get("ammo"),
                    "labour": basic_data.get("labour")
                },
                "attack_attributes": {
                    "piercing_armour_penetration": basic_data.get("piercing_armour_penetration"),
                    "slashing_armour_penetration": basic_data.get("slashing_armour_penetration"),
                    "blunt_armour_penetration": basic_data.get("blunt_armour_penetration"),
                    "piercing_damage": basic_data.get("piercing_damage"),
                    "slashing_damage": basic_data.get("slashing_damage"),
                    "blunt_damage": basic_data.get("blunt_damage")
                },
                "defence_attributes": {
                    "piercing_defence": basic_data.get("piercing_defence"),
                    "slashing_defence": basic_data.get("slashing_defence"),
                    "blunt_defence": basic_data.get("blunt_defence"),
                    "block": basic_data.get("block"),
                    "block_recovery": basic_data.get("block_recovery")
                },
            },
            "unit_type": main_data.get("unit_type"),
            "icon_path": main_data.get("icon_path"),
            "tier": main_data.get("tier"),
            "max_level": main_data.get("max_level"),
            "strength": basic_data.get("strength"),
            "leadership": basic_data.get("leadership"),
            "formations": basic_data.get("formations"),
            "orders": basic_data.get("orders"),
            "traits": basic_data.get("traits"),
        },
    }