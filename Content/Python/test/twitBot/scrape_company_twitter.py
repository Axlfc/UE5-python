# coding=utf-8
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import os

def get_source(url):
    """Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.',
                      'https://google.',
                      'https://webcache.googleusercontent.',
                      'http://webcache.googleusercontent.',
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links


def get_results(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    return response


def parse_results(response):
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"

    results = response.html.find(css_identifier_result)

    output = []

    for result in results:
        item = {
            'link': result.find(css_identifier_link, first=True).attrs['href']
        }

        output.append(item)

    return output


def google_search(query):
    return parse_results(get_results(query))


def scrape_companies():
    companies = ["0verflow", "11 bit studios", "1C Company", "1-Up Studio", "2K Czech", "2K", "343 Industries",
                 "38 Studios", "3D Realms", "42 Entertainment", "4A Games", "5th Cell", "989 Studios",
                 "Acclaim Entertainment", "Acclaim Studios Austin", "Accolade", "Access Games", "Access Software",
                 "ACE Team", "Aces Game Studio", "Acquire", "Action Forms", "Active Gaming Media", "Activision",
                 "Adventure Soft", "Akella", "Alfa System", "AlphaDream", "Amazon Game Studios", "Animation Magic",
                 "Amazon Game Studios, Orange County (formerly Double Helix Games)", "Ambrella", "Amusement Vision",
                 "Ancient", "Anino", "Ankama Games", "Appy Entertainment", "AQ Interactive", "Aquria",
                 "Arc System Works", "Arcane Kids", "Arcen Games", "Arkane Studios", "Arkedo Studio", "ArenaNet",
                 "Arika", "Art Co., Ltd", "Artech Digital Entertainment", "Artdink", "ArtePiazza", "Artificial Studios",
                 "Artoon", "Arzest", "Ascaron", "Asobo Studio", "Aspyr",
                 "Atari Interactive (formerly Hasbro Interactive)", "Atlus", "Atomic Planet Entertainment",
                 "Attic Entertainment Software", "Audiogenic", "Avalanche Studios Group", "Aventurine SA", "Babaroga",
                 "Backflip Studios", "Bandai Namco Entertainment", "Bandai Namco Studios", "Bauhaus Entertainment",
                 "B.B. Studio", "Beamdog", "Beenox", "Behaviour Interactive", "Behaviour Santiago",
                 "Bethesda Game Studios", "Big Blue Bubble", "Big Finish Games", "Big Huge Games", "BioWare",
                 "The Bitmap Brothers", "Best Way", "Bits Studios", "Bizarre Creations", "Black Forest Games",
                 "Black Isle Studios", "Black Rock Studio", "Black Wing Foundation", "Blind Squirrel Games",
                 "Blitz Games Studios", "Blizzard Entertainment", "Bloober Team", "Bluepoint Games", "Blueside",
                 "Blue Fang Games", "Blue Tongue Entertainment", "Bluehole Studio", "Bohemia Interactive",
                 "Boss Fight Entertainment", "Boss Key Productions", "BreakAway Games", "Brøderbund",
                 "Budcat Creations", "Bugbear Entertainment", "Bullfrog Productions", "Bungie",
                 "Camelot Software Planning", "Capcom", "Capcom Vancouver", "Carbine Studios", "Cattle Call",
                 "Cauldron", "Cave", "Cavia", "CCP Games", "CD Projekt Red", "Certain Affinity", "Chair Entertainment",
                 "Chunsoft", "Cing", "Clap Hanz", "Climax Entertainment", "Climax Studios", "Clover Studio",
                 "Coded Illusions", "Codemasters", "Coffee Stain Studios", "Cohort Studios", "Coktel Vision",
                 "Colossal Order", "Compile Heart", "Compulsion Games", "Com2uS", "Core Design", "Crafts & Meister",
                 "Crawfish Interactive", "Creat Studios", "Creative Assembly", "Creatures", "Criterion Games",
                 "Croteam", "Cryo Interactive", "Culture Brain Excel", "Crea-Tech", "Cryptic Studios",
                 "Crystal Dynamics", "Crytek", "Crytek UK", "Cyan Worlds", "Cyanide", "CyberConnect2",
                 "Cyberlore Studios (Blueline Simulations[9])", "CyberStep", "Cygames", "Dambuster Studios",
                 "Danger Close Games", "Day 1 Studios", "Daybreak Game Company", "Deadline Games", "Deck13",
                 "Deep Silver Volition", "Demiurge Studios", "DeNA", "devCAT Studios (Nexon development 3rd division)",
                 "Dhruva Interactive", "Die Gute Fabrik", "Digital Extremes", "Digital Eclipse", "Digitalmindsoft",
                 "Digital Reality", "Dimps", "Disney Interactive Studios", "Don Bluth Entertainment", "Don't Nod",
                 "DotEmu", "Double Fine Productions", "Dynamix", "Dovetail Games", "The Dovetail Group", "EA Black Box",
                 "EA Digital Illusions CE (EA DICE)", "EA Gothenburg", "EA Phenomic", "EA Salt Lake", "EA Tiburon",
                 "EA Vancouver (formerly Distinctive Software)", "Eat Sleep Play", "Eko Software", "Egosoft",
                 "Eden Games", "Eidos-Montréal", "Eighting", "Electronic Arts", "Elemental Games", "Elite Systems",
                 "Engine Software", "Ensemble Studios", "Epic Games", "Epics", "Epicenter Studios",
                 "ESA (formerly Softmax)", "Eric Barone", "Epyx", "Étranges Libellules", "Eugen Systems", "Eurocom",
                 "Evolution Studios", "Examu", "Eyedentity Games", "F4", "Facepunch Studios", "FarSight Studios",
                 "FASA Studio", "Fatshark", "feelplus", "Felistella", "Firaxis Games", "Firefly Studios", "Firesprite",
                 "First Star Software", "Flagship Studios", "Flight-Plan", "Flying Wild Hog", "Focus Entertainment",
                 "Foundation 9 Entertainment", "Fox Digital Entertainment", "FoxNext", "Frictional Games", "Frogwares",
                 "Frog City Software", "FromSoftware", "Frontier Developments", "Frozenbyte", "FTL Games", "Fun Labs",
                 "Funcom", "FuRyu", "Futuremark", "Gaijin Entertainment", "Game Arts", "Game Freak", "GameHouse",
                 "Gameloft", "Gamevil", "Ganbarion", "Gearbox Software", "Geewa", "Genius Sonority", "Genki",
                 "Glu Mobile", "Gogii Games", "Good-Feel", "Goodgame Studios", "Granzella", "Grasshopper Manufacture",
                 "Gravity", "Gray Matter Studios", "Gremlin Interactive", "Grezzo", "Grin", "Grinding Gear Games",
                 "Griptonite Games", "GSC Game World", "Guerrilla Cambridge", "Guerrilla Games", "Gunfire Games",
                 "GungHo Online Entertainment", "Gust", "Haemimont Games", "HAL Laboratory", "Halfbrick", "Hanaho",
                 "h.a.n.d.", "Hangar 13", "Harebrained Schemes", "Harmonix Music Systems", "Hazelight Studios",
                 "Headstrong Games", "Heartbeat", "Heavy Iron Studios", "HB Studios", "HeroCraft", "HexaDrive",
                 "High Impact Games", "High Moon Studios", "High Voltage Software", "Hothead Games", "Housemarque",
                 "Hudson Soft", "Human Entertainment", "Human Head Studios", "Humongous Entertainment",
                 "Hyperion Entertainment", "Ice-Pick Lodge", "id Software", "Idea Factory", "Idol Minds", "Imageepoch",
                 "Image & Form", "Imagineer", "Infinity Ward", "Infocom", "Incognito Entertainment",
                 "Incredible Technologies", "indieszero", "Innerloop Studios", "Insomniac Games", "Intelligent Systems",
                 "Interplay Entertainment", "Introversion Software", "inXile Entertainment", "IO Interactive",
                 "Ion Storm", "Ion Storm Austin", "Irem", "Iron Galaxy Studios", "Iron Lore Entertainment",
                 "Irrational Games", "Ivory Tower", "Jackbox Games", "Jadestone Group", "Jagex", "Jaleco", "Jam City",
                 "Javaground", "Jupiter", "JV Games", "Kairosoft", "Kalypso Media", "Kaos Studios",
                 "Keen Software House", "Kesmai", "Kiloo Games", "King", "Klei Entertainment",
                 "Koei Tecmo Games (formerly Koei)", "KOG Studios", "Kojima Productions", "Konami", "Kongzhong",
                 "Krome Studios", "Krome Studios Melbourne", "Kuju Entertainment", "Kunos Simulazioni", "Kush Games",
                 "Kuma Reality Games", "Kylotonn", "Larian Studios", "Left Field Productions", "Legacy Interactive",
                 "Legend Entertainment", "Legendo Entertainment", "Level-5", "Lift London", "Limbic Entertainment",
                 "Lionhead Studios", "Liquid Entertainment", "Little Green Men Games", "LK Avalon", "Llamasoft",
                 "Linden Lab", "Locomotive Games", "Looking Glass Studios", "Love-de-Lic", "LucasArts", "Luma Arcade",
                 "Luxoflux", "MachineGames", "Magenta Software", "MAGES.", "Majesco Entertainment", "Marvelous",
                 "Massive Entertainment", "Masthead Studios", "Matrix Software", "Maxis", "Mean Hamster Software",
                 "Media Molecule", "Media.Vision", "Mediatonic", "MegaZebra", "Mercury Steam", "Metropolis Software",
                 "MicroProse Software", "Microsoft Casual Games", "Midway Games", "Midway Studios – Newcastle",
                 "Might and Delight", "miHoYo", "Milestone", "Milestone srl", "Mimimi Games", "Mistwalker",
                 "Mitchell Corporation", "MLB Advanced Media", "Mode 7 Games", "Mojang AB", "Monolith Productions",
                 "Monolith Soft", "Monster Games", "Monte Cristo", "Moonton", "Moon Studios", "Motion Twin", "MTO",
                 "Mythic Entertainment", "Nadeo", "Namco Tales Studio", "Nanobit", "NAPS team", "Natsume",
                 "NaturalMotion", "Naughty Dog", "NCSoft", "NDcube", "NDOORS Corporation", "Neko Entertainment",
                 "Nerve Software", "NetDevil", "NetDragon Websoft", "NetEase", "NetherRealm Studios", "Neverland",
                 "Neversoft", "Nevosoft", "New World Computing", "New World Interactive", "Nexon", "Nexon Korea",
                 "Next Level Games", "Niantic", "Nibris", "Nicalis", "Night School Studio", "Nihon Falcom",
                 "Nikita Online", "Nimble Giant Entertainment", "Ninjabee", "Ninja Theory", "Nintendo",
                 "Nintendo Software Technology", "Nippon Ichi Software", "Nival", "Nordeus", "NovaLogic", "Novarama",
                 "Now Production", "Nude Maker", "NuFX", "n-Space", "Obsidian Entertainment", "Oddworld Inhabitants",
                 "Omega Force", "Origin Systems", "OtherSide Entertainment", "Outfit7", "Outrage Entertainment",
                 "Out of the Park Developments", "Overkill Software", "Oxygen Studios", "Page 44 Studios",
                 "Pangea Software", "Paradigm Entertainment", "People Can Fly", "Planetarium", "Project Sora",
                 "Purple Lamp Studios", "Papaya Studio", "Project Soul", "Panther Games Pty Ltd",
                 "Paradox Development Studio", "Parallax Software", "Pandemic Studios", "Pendulo Studios",
                 "Penguin Software", "Perfect World", "Petroglyph", "Phantagram", "Pipeworks Studios", "Piranha Bytes",
                 "Piranha Games", "Pi Studios", "Pivotal Games", "Pixel Federation", "Playdom", "Playfish", "PlayFirst",
                 "Playground Games", "PlatinumGames", "Polyphony Digital", "PopCap Games", "PopTop Software",
                 "Press Play", "Psyonix", "PUBG Studios", "Punch Entertainment", "Pyro Mobile", "Q Entertainment",
                 "Q-Games", "Quantic Dream", "Quest Corporation", "Quintet", "Radical Entertainment", "Rage Games",
                 "Rainbow Studios", "Rare", "Raven Software", "RDI Video Systems", "Ready at Dawn", "Red Entertainment",
                 "Reality Pump Studios", "Realtime Associates", "Realtime Worlds", "Rebellion Developments",
                 "Rebellion Warwick", "RedLynx", "Red Thread Games", "Red Storm Entertainment", "RedTribe (Tribalant)",
                 "Reflexive Entertainment", "Relic Entertainment", "Remedy Entertainment", "Respawn Entertainment",
                 "Reto-Moto", "Retro Studios", "Revolution Software", "Riot Games", "Rising Star Games", "Robomodo",
                 "Robot Entertainment", "Rockstar Games", "Rockstar India", "Rockstar Leeds", "Rockstar Lincoln",
                 "Rockstar London", "Rockstar New England", "Rockstar North", "Rockstar San Diego", "Rockstar Toronto",
                 "Rockstar Dundee", "Rocksteady Studios", "Robinson Technologies", "Rovio Entertainment", "Runic Games",
                 "Running with Scissors", "Saber Interactive", "Sand Grain Studios", "Sandlot", "Sanzaru Games",
                 "Sir-Tech", "Schell Games", "SCS Software", "Sega", "SEGA AM R&D Division 1 (Sega AM1)",
                 "SEGA AM R&D Division 2 (Sega AM2)", "Sega AM3", "Sega CS Research and Development No. 2 (Sonic Team)",
                 "Sega Sports R&D", "Sensible Software", "Bend Studio",
                 "San Mateo Studio (formerly Foster City Studio)", "Japan Studio", "London Studio", "San Diego Studio",
                 "Santa Monica Studio", "Studio Liverpool", "Shaba Games", "SIE Worldwide Studios", "SingleTrac",
                 "Shengqu Games", "Sherman3D", "Shin'en Multimedia", "Sierra Entertainment", "Silicon Knights",
                 "Silicon Studio", "Simtex", "skip Ltd.", "Slant Six Games", "Sledgehammer Games", "Snail",
                 "Snapshot Games", "Slightly Mad Studios", "Slipgate Ironworks", "Slitherine Software", "Smilegate",
                 "SNK", "Sobee Studios", "Snowblind Studios", "Software 2000", "Sony Interactive Entertainment",
                 "Sora Ltd.", "Spellbound Entertainment", "Spiders", "Spike", "Spike Chunsoft", "Spil Games",
                 "Splash Damage", "Sports Interactive", "Sproing Interactive Media", "Square Enix", "Squad",
                 "Stainless Games", "Stainless Steel Studios", "Starbreeze Studios", "Stardock", "Sting Entertainment",
                 "Strategic Simulations", "Stoic Studio", "Strawdog Studios", "Straylight Studios",
                 "Streamline Studios", "Success", "Sucker Punch Productions", "Sumo Digital", "Sunsoft", "Supercell",
                 "Supermassive Games", "Supergiant Games", "SuperVillain Studios", "Survios", "Studio Wildcard",
                 "Swordfish Studios", "Swingin' Ape Studios", "StormRegion", "Sunstorm Interactive", "Syn Sophia",
                 "SystemSoft Beta", "Taito", "Tango Gameworks", "Tag Games", "TaleWorlds Entertainment", "Tamsoft",
                 "T&E Soft", "Tantrumedia", "Tantalus Media", "Tarsier Studios", "Tate Multimedia", "Team17",
                 "Team Asobi", "Team Bondi", "Team Ico", "Team Ninja", "Techland", "Tecmo", "Telltale Games", "Tencent",
                 "Tencent Games", "Tequila Works", "Terminal Reality", "Tetris Online", "Teyon", "Thatgamecompany",
                 "The Chinese Room", "The Coalition", "The Farm 51", "The Initiative", "THQ", "THQ Nordic",
                 "Three Fields Entertainment", "Three Rings Design", "TimeGate Studios", "TiMi Studios", "Toaplan",
                 "Toby Fox", "ToeJam & Earl Productions", "Tokyo RPG Factory", "Toolworks", "TopWare Interactive",
                 "Torpex Games", "Torus Games", "Tose", "Toys for Bob", "Trapdoor", "Transmission Games",
                 "Traveller's Tales", "Treyarch", "Treasure", "tri-Ace", "tri-Crescendo", "Trion Worlds",
                 "Tripwire Interactive", "Triumph Studios", "Turn 10 Studios", "Turtle Rock Studios",
                 "Two Point Studios", "Two Tribes", "Typhoon Games (HK)", "Ubisoft", "Ubisoft Blue Byte",
                 "Ubisoft Leamington", "Ubisoft Reflections", "UEP Systems", "Ultimate Play the Game", "Undead Labs",
                 "Underground Development", "United Front Games", "United Game Artists", "Universomo",
                 "Unknown Worlds Entertainment", "Valhalla Game Studios", "Valve", "Vanillaware", "Vanpool",
                 "Venan Entertainment", "Vic Tokai", "Vicarious Visions", "Vigil Games", "Virtual Heroes", "Virtuos",
                 "Visceral Games", "Visual Concepts", "Vostok Games", "VoxelStorm", "Wahoo Studios", "Warhorse Studios",
                 "Wargaming", "Wargaming Saint Petersburg", "Wargaming Seattle",
                 "Warner Bros. Interactive Entertainment", "WB Games Boston (formerly Turbine)",
                 "WB Games - Avalanche (formerly Avalanche Software)", "Webfoot Technologies", "WeMade",
                 "Westone Bit Entertainment", "Westwood Studios", "Wideload Games", "Wildfire Studios",
                 "Wizet studio (Nexon development 1st division)", "Wolfire Games", "World Forge", "Xbox Game Studios",
                 "XPEC Entertainment", "Yager Development", "Yuke's", "ZeniMax Online Studios", "Zen Studios",
                 "Zipper Interactive", "Zombie Studios", "ZootFly", "Zynga"]
    twitter_handles = []
    for company in companies:
        result = google_search(company + " Video Game Company")
        for line in result:
            if "twitter" or "Twitter" in line:
                text = list(line.values())
                for word in text:
                    if "https://" in word:
                        if "twitter.com" in word:
                            print(word.replace("https://twitter.com/", "").replace("?lang=es", "").replace(
                                "https://mobile.twitter.com/", ""))
                            twitter_handles.append(
                                word.replace("https://twitter.com/", "").replace("?lang=es", "").replace(
                                    "https://mobile.twitter.com/", ""))

    print(twitter_handles)
    with open('handles.txt', 'w') as f:
        for twitterhandle in twitter_handles:
            f.write(twitterhandle + '\n')


def create_company_script(companyname):
    # Create python script with the import and
    if not os.path.exists("temp"):
        os.mkdir("temp")
    filename = "temp" + "\\" + companyname + ".py"
    with open(filename, "w", encoding='UTF-8') as w:
        t = "import sys\n" \
            "sys.path.append(\"..\")\n" \
            "import twit as twitter\n" \
            "print(twitter.get_name(\"" + companyname + "\"))\n" \
            "print(twitter.get_webpage(\"" + companyname + "\"))\n" \
            "print(\"\\n\")"
        w.write(t)
    # return twitter.get_webpage(companyname)


def createWinScript(pythonScripts):
    filename = "temp" + "\\" + "runPythonScript.ps1"
    with open(filename, "w", encoding='UTF-8') as w:
        t1 = "function Run-Python-Script {\n" \
            "   Param(\n" \
                "\t[Parameter(Mandatory=$true,Position=0)] [String]$ScriptName\n" \
            "   )\n" \
            "   python $ScriptName\n" \
            "}\n" \
            "\n" \
            "$pythonScripts =\n"
        str1 = ""
        for pythonScript in pythonScripts:
            str1 += "\"" + pythonScript + "\",\n"

        t2 = "foreach ($pythonScript in $pythonScripts)\n" \
            "{\n" \
            "\tWrite-Host $pythonScript\n" \
            "\tRun-Python-Script $pythonScript\n" \
            "}\n"

        t = t1 + str1[:-2] + "\n" + t2

        w.write(t)


def main():
    lines = ["overflowsweden", "1upgamesstudio", "lab42games", "4agames", "5thcell", "theaceteam", "gameacestudio", "team_agm_en", "amzngamestudios", "aninogames", "appy", "arcengames", "arkedostudio", "arenanet", "visualartsusa", "atlus_west", "babarogatweet", "backflipstudios", "bandainamcous", "behaviour", "behaviourcl", "bethesdastudios", "bigbluebubble", "bigfinishgames", "bighugegames", "best_way_games", "11bitstudios", "bizarrec", "blackforestteam", "blackislestudio", "blackrockster", "blind_squirrel_", "_bgs_", "blooberteam", "bohemiainteract", "bossfightent", "bosskey", "breakawaygames", "bugbeargames", "capcomvancouver", "carbine_studios", "cauldronlondon", "cdprojektred", "certainaffinity", "chairgames", "hanz_en", "climaxstudios", "codemasters", "coffee_stain", "studiocohort", "compulsiongames", "com2us", "coredesign_com", "creatstudios", "croteam", "crypticstudios", "cyanidestudio", "cc2information", "dsdambuster", "deck13_de", "dsvolition", "demiurgestudios", "gutefabrik", "digitalextremes", "digitalmindsoft", "dotemu", "dovetailgames", "dovetailgames", "eko_software", "edengames", "enginesoftware", "concernedape", "eugensystems", "fatsharkgames", "firaxisgames", "fireflyworlds", "flying_wild_hog", "focus_entmt", "frictionalgames", "frogwares", "frozenbyte", "gaijinent", "gameloft_spain", "geewa", "genki_jpn", "glumobile", "grasshopper_en", "gunfire_games", "haemimontgames", "halfbrick", "hangar13games", "webeharebrained", "hazelightgames", "hb_studios", "highmoonstudios", "hotheadgames", "humanheadgames", "humongousent", "icepicklodge", "idsoftware", "steamworldgames", "incrediblegames", "innerloopstudi1", "interplaygames", "ivsoftware", "ivorytoweroffic", "jagex", "jamcityhq", "kalypsomedia", "kiloogames", "kromestudios", "kujuonline", "kylotonn_games", "legendogames", "level5_ia", "lgmgames", "robustgames", "poondonkus", "lumaarcade", "machinegames", "magentasoftware", "magecompany", "majesco", "marvelous_games", "ubimassive", "mediatonic", "megazebra", "mercurysteam", "milestoneitaly", "milestoneitaly", "mimimiprod", "mistwalker", "monolithdev", "montecristo", "moongamestudios", "motiontwin", "nanobitgames", "napsteam", "natsume_inc", "nmgames", "nekoent", "nervesoftware", "netherrealm", "nightschoolers", "nimblegiantent", "ninjabeegames", "novarama", "n_space", "otherside_games", "overkill_tm", "planetariumhq", "purple_lamp", "panthergames", "pdx_dev_studio", "perfectworldcn", "petroglyphgames", "piranha_bytes", "piranhagames", "pixelfederation", "playfish", "weareplayground", "pressplaynews", "psyonixstudios", "punchgames", "rainbowstudios", "rad_studios", "reality_pump", "redthreadgames", "relicgames", "retomoto", "retrostudios", "revsoftgames", "riotgames", "risingstargames", "robomodo", "robotent", "ruffiangames", "rocksteadygames", "rtsoft", "sabergames", "sanzarugames", "schellgames", "sonysantamonica", "zhugeex", "sherman3d", "shinengames", "shgames", "snailgamesusa", "snapshot_games", "slightlymadteam", "smilegateb", "spidersgames", "spikechunsoft_e", "splashdamage", "sigames", "sproinggames", "squaddevs", "stainless_games", "starbreezeab", "stoicstudio", "straylightcraft", "suckerpunchprod", "supergiantgames", "svsgames", "survios", "wildcardstudios", "tangogameworks", "taggames", "tantalus_games", "tarsierstudios", "tatemultimedia", "teambondi", "techlandgames", "koeitecmous", "tequilaworks", "teyongames", "thatgamecompany", "coalitiongears", "thefarm51", "theinitiative", "3fieldsent", "threerings", "timegatestudios", "timistudios", "topwareusa", "torusgames", "trapdoorgames", "tri_crescendo", "tripwireint", "triumphstudios", "turn10studios", "turtlerock", "twopointstudios", "twotribesgames", "ubisoftbluebyte", "ubileam", "ubireflections", "undeadlabs", "unitedfrontgame", "unknownworlds", "valvesoftware", "vvisionsstudio", "vc_novato", "vostokgames", "voxelstorm", "avalanchewb", "webfootgames", "wideloadgames", "wolfire", "yagerdev", "yukes_aew", "zenimax_online"]

    for user in range(len(lines)):
        create_company_script(lines[user])

    pythonScripts = []
    for pythonScript in os.listdir("temp"):
        pythonScripts.append(pythonScript)
    createWinScript(pythonScripts)


if __name__ == '__main__':
    main()