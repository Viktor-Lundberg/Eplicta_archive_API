# Eplicta_archive_API
Skript för att kommunicera med Eplictas API (Azure Blobstorage) samt för att generera arkivversioner av från API:et nedladdade socialamedie-konton, både som xml och som html.   


## Innehåll
* **Connect_to_API.py** = Anropar Eplictas API och hämtar blobar och bloblistor 
* **Select_blobs_from_bloblist_xml.py** = Används för att med hjälp av nedladdad bloblista välja ut de inlägg som ska ingå i arkiveringen, samt skapar en txt-fil som kan användas för nedladdning av rätt blobar via API:et. 
* **Generate_xml.py** = Skapar själva arkivpaketet. Skriptet öppnar nedladdade blobzippar och slår ihop xmlfilerna till en stor xmlfil över den nedladdade kanalens innehåll och lägger bifogade filer i en content mapp. 
* **Generate_html.py** = Skapar en html-sida över arkivpaketet för att visualisera den arkiverade kanalen och underlätta tillgängliggörandet av arkivpaketet. Skriptet öppnar genererad xml-fil och content-mapp och skapar en html-sida av det arkiverade kontot.  

### Exempel på körschema
1. Använd Connect_to_API.py för att hämta hem en xml-fil med Blobar från API:et
1. Kör Select_blobs_from_bloblist_xml.py för att välja ut de blobar (inlägg) som ska laddas ner och ingå i arkivpaketet.
1. Kör Connect_to_API.py för att hämta hem de utvalda Blobarna. 
1. Kör Generate_xml.py för att skapa arkivpaketet (en stor xml-fil och en content-mapp med bilagor).
1. Kör Generate_html.py för att skapa en html-version av kanalen.