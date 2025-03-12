# Precinct Level Election Returns
The goal of this project is to gather, parse, process, and validate the precinct level returns from the 2024 election. Starting with the state of Pennsylvania. To, hopefully, speed this up I'm trying to leverage generative AI models, when possible, for automating some of the parsing and processing steps. 

As of now, there is a consistently performing prompt-based approach for parsing "single precinct per page" (SPPP) type PDF return documents.

Raw data has been gathered for all counties in PA, save for 6 counties which lack precinct-level return data. 
* 015	Bradford County
* 031	Clarion County
* 037	Columbia County
* 043	Dauphin County
* 063	Indiana County
* 113	Sullivan County

**Of note is the fact that these counties contain roughly 230,000 likely voters in a race decided by 120,000 votes.** 

# Method
* **Parsing** 
  * Converting the raw return data into a common format.
  * *Progress*
    * Working SPPP parser.
    * Working ClarityElection xml parser. 
* **Processing** 
  * Converting races, parties, candidates to common values. 
  * Associating precincts with 2020 VTDST20 identifiers (when possible).
  * Extracting formatted data from the aggregated processed data. 
  * *Progress*
    * Draft pipeline for associating VTDST20 identifiers. 
* **Validation**
  * Pipeline for randomly selecting target data to validate manually.
  * *Progress*
    * None. Oof.

# PA Progress
The following table contains the current progress in parsing and processing the county precinct data.

| FIPS | County                | Raw Data | Src                                                                                                                                | Type         | Parsed | Notes                                                                                                                                      |
| ---- | --------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 001  | Adams County          | X        | [Link](https://www.adamscountypa.gov/departments/electionsandvoterregistration/electionresults)                                    | SPPP         | X      |                                                                                                                                            |
| 003  | Allegheny County      | X        |                                                                                                                                    | CEXML        | X      |                                                                                                                                            |
| 005  | Armstrong County      | X        |                                                                                                                                    | Folder       |        |                                                                                                                                            |
| 007  | Beaver County         | X        | [Link](https://www.beavercountypa.gov/departments/election-bureau/election-results)                                                | SPPP         | X      |                                                                                                                                            |
| 009  | Bedford County        | X        |                                                                                                                                    | TERROR       |        |                                                                                                                                            |
| 011  | Berks County          | X        | [Link](https://www.berkspa.gov/departments/election-services/election-results)                                                     | SPPP         | X      |                                                                                                                                            |
| 013  | Blair County          | X        | [Link](https://www.blairco.org/departments/elections-voter-registration/election-results)                                          | SPPP         | X      |                                                                                                                                            |
| 015  | Bradford County       | M        | [Link](https://bradfordcountypa.org/department/elections/)                                                                         | No PLD       |        | No precinct data. Other years have it. Email.                                                                                              |
| 017  | Bucks County          | X        |                                                                                                                                    | UNQ?         |        |                                                                                                                                            |
| 019  | Butler County         | X        | [Link](https://www.butlercountypa.gov/683/Election-Returns-2021---Present)                                                         | SPPP         | X      |                                                                                                                                            |
| 021  | Cambria County        | X        |                                                                                                                                    | CEXML        | X      |                                                                                                                                            |
| 023  | Cameron County        | X        |                                                                                                                                    | Folder       |        |                                                                                                                                            |
| 025  | Carbon County         | X        |                                                                                                                                    | TERROR       |        |                                                                                                                                            |
| 027  | Centre County         | X        | [Link](https://centrecountypa.gov/3498/2024-General-Election-Official-Results)                                                     | SPPP         | X      |                                                                                                                                            |
| 029  | Chester County        | X        | [Link](https://www.chesco.org/156/Voter-Services)                                                                                  | SPPP         | X      |                                                                                                                                            |
| 031  | Clarion County        | M        | [Link](https://www.co.clarion.pa.us/government/departments/elections__voter_registration/archived_election_results.php#outer-1333) | No PLD       |        | No precinct data. Past years have it.                                                                                                      |
| 033  | Clearfield County     | X        | [Link](https://clearfieldcountypa.gov/199/Election-Results)                                                                        | SPPP         | X      |                                                                                                                                            |
| 035  | Clinton County        | X        |                                                                                                                                    | Folder       |        |                                                                                                                                            |
| 037  | Columbia County       | M        | [Link](http://www.columbiapa.org/voter/archive.php)                                                                                | No PLD       |        | Same format as Clarion and Bradford                                                                                                        |
| 039  | Crawford County       | X        | [Link](https://www.crawfordcountypa.net/VoterServices/Pages/Election-Results.aspx)                                                 | UNQ?         |        |                                                                                                                                            |
| 041  | Cumberland County     | X        | [Link](https://www.cumberlandcountypa.gov/3135/Election-Results)                                                                   | SPPP         | X      |                                                                                                                                            |
| 043  | Dauphin County        | M        | [Link](https://www.dauphinc.org/election)                                                                                          | No PLD       |        | The link to the returns gives a 500 eventually. Missing ANY election info. 200k people. that's a lot. get ISE when we navigate to results. |
| 045  | Delaware County       | X        | [Link](https://results.enr.clarityelections.com/PA/Delaware/122488/web.345435/#/summary)                                           | CEXML        | X      |                                                                                                                                            |
| 047  | Elk County            | X        | [Link](https://www.co.elk.pa.us/index.php/election-results)                                                                        | UNQ?         |        | Looks SIMILAR to a SPPP, but has so many write-ins that it splits the tables. Blarg.                                                       |
| 049  | Erie County           | X        | [Link](https://results.enr.clarityelections.com/PA/Erie/122589/web.345435/#/summary)                                               | CEXML-WI     | X      | This contains writeins, might have to tweak the script?                                                                                    |
| 051  | Fayette County        | X        | [Link](https://results.enr.clarityelections.com/PA/Fayette/122836/web.345435/#/summary)                                            | CEXML-WI     | X      | CE with writeins, again.                                                                                                                   |
| 053  | Forest County         | X        | [Link](https://www.co.forest.pa.us/departments/election_results.php#revize_document_center_rz1455)                                 | Folder       |        | Folder of SPPP's                                                                                                                           |
| 055  | Franklin County       | M        | [Link](https://www.franklincountypa.gov/departments/elections-voter-registration/)                                                 | SPPP         |        | Found it.                                                                                                                                  |
| 057  | Fulton County         | X        | [Link](https://www.co.fulton.pa.us/elections-enr-2024b.php)                                                                        | Folder       |        | Folder of unq SPPPs. might need it's own prompt.                                                                                           |
| 059  | Greene County         | X        | [Link](https://greenecountypa.gov/elections/Default.aspx?PageLayout=PRECINCTS&Election=20062)                                      | Website List |        | Its a list of just fucking HTML pages. Nothing to download.                                                                                |
| 061  | Huntingdon County     | X        | [Link](https://www.huntingdoncounty.net/departments/elections/elections-archive)                                                   | SPPP         | X      | They don't have an election page. just get the pdf from google?                                                                            |
| 063  | Indiana County        | M        | [Link](https://www.indianacountypa.gov/departments/voting-and-elections/elections/)                                                | No PLD       |        | No link on their election page to any kind of results. Just county level results on the state site.                                        |
| 065  | Jefferson County      | X        | [Link](https://www.jeffersoncountypa.gov/wp-content/uploads/2024/11/StatementOfVotesCastRPTOFFICALRESULTS.pdf)                     | TERROR       |        | AHHHH                                                                                                                                      |
| 067  | Juniata County        | X        | [Link](https://www.juniataco.org/departments/voter-registration/election-dates-results/)                                           | SPPP         | X      | Looks like an easy one.                                                                                                                    |
| 069  | Lackawanna County     | X        | [Link](https://www.lackawannacounty.org/government/departments/elections/general_election_results_november_5_2024.php)             | SPPP         | X      |                                                                                                                                            |
| 071  | Lancaster County      | X        | [Link](https://electionresults.lancastercountypa.gov/results/public/lancaster-county-pa/elections/2024GeneralElection)             | UNQ?         |        | JSON?!?!? what.the.fuck. The media export at the bottom. By these wonderful asshats: [Enhanced Voting](https://www.enhancedvoting.com/)    |
| 073  | Lawrence County       | X        | [Link](https://lawrencecountypa.gov/departments/voter-elections/election-results)                                                  | SPPP         | X      | Might need to tweak to deal with the 'summary' section?                                                                                    |
| 075  | Lebanon County        | X        | [Link](https://www.lebanoncountypa.gov/departments/voter-registration/election-results)                                            | SPPP         | X      |                                                                                                                                            |
| 077  | Lehigh County         | X        | [Link](https://www.livevoterturnout.com/ENR/lehighpaenr/8/en/Index_8.html)                                                         | CSV          |        | DEAR SWEET LORD!. Its already in a csv in the proper format YAY. just convert to our common format.                                        |
| 079  | Luzerne County        | X        | [Link](https://results.enr.clarityelections.com/PA/Luzerne/122840/web.345435/#/summary)                                            | CEXML-WI     | X      | CE with Write-ins                                                                                                                          |
| 081  | Lycoming County       | X        | [Link](https://www.lyco.org/Departments/Voter-Services/Results-From-Previous-Elections)                                            | UNQ?         |        | Its that 'well formatted sections per precinct' format. We've seen another like this.                                                      |
| 083  | McKean County         | X        | [Link](https://www.mckeancountypa.gov/news_detail_T8_R8.php)                                                                       | SPPP         | X      |                                                                                                                                            |
| 085  | Mercer County         | X        | [Link](https://www.mercercountypa.gov/election/)                                                                                   | SPPP         | X      | Also has summary sections                                                                                                                  |
| 087  | Mifflin County        | X        | [Link](https://www.mifflincountypa.gov/voter-registration-elections/election-central)                                              | SPPP         | X      |                                                                                                                                            |
| 089  | Monroe County         | M        | [Link](https://agencies2.monroecountypa.gov/elections/)                                                                            | HTML         |        | We could grab the stuff from each drop down and parse it. The web app has precinct data. Otherwise, we'd need to email to get a pdf/csv    |
| 091  | Montgomery County     | X        | [Link](https://www.montgomerycountypa.gov/753/Voter-Services)                                                                      | TERROR       |        | Jesus christ it's worse than I remember.                                                                                                   |
| 093  | Montour County        | X        | [Link](https://www.montourcounty.gov/departments/elections/results)                                                                | SPPP         | X      |                                                                                                                                            |
| 095  | Northampton County    | X        | [Link](https://www.norcopa.gov/election-result)                                                                                    | SPPP         | X      |                                                                                                                                            |
| 097  | Northumberland County | X        | [Link](https://northumberlandcountypa.gov/prior-results/)                                                                          | SPPP         | X      |                                                                                                                                            |
| 099  | Perry County          | X        | [Link](https://perryco.org/departments/elections-voter-registration/)                                                              | UNQ?         |        | The kind with the wellformed headers/sections?                                                                                             |
| 101  | Philadelphia County   | X        | [Link](https://vote.phila.gov/results/)                                                                                            | UNQ?         |        | Its a folder of per-race excel sheets. Oof.                                                                                                |
| 103  | Pike County           | X        | [Link](https://www.pikepa.org/government/elections_office/past_election_results.php#outer-372sub-418)                              | UNQ?         |        | Per-Race Precinct Tables, but splits pages. Blarg.                                                                                         |
| 105  | Potter County         | X        | [Link](https://pottercountypa.gov/departments/elections/)                                                                          | SPPP         | X      | With summary chunk.                                                                                                                        |
| 107  | Schuylkill County     | X        | [Link](http://www.co.schuylkill.pa.us/info/Offices/Election/Election/Results/Info.csp)                                             | Folder       |        | Folder of HTML TABLES. Jesus Christ. This is so fucking bad.                                                                               |
| 109  | Snyder County         | X        | [Link](https://www.snydercounty.org/departments/elections/)                                                                        | SPPP         | X      |                                                                                                                                            |
| 111  | Somerset County       | X        | [Link](http://www.co.somerset.pa.us/pages/voters/electionresults.asp)                                                              | Folder       |        | Folder of kinda SPPP files? Mehhhh                                                                                                         |
| 113  | Sullivan County       | M        | [Link](https://www.sullivancountypa.gov/offices/election-bureau)                                                                   | No PLD       |        | No election-specific contact info?                                                                                                         |
| 115  | Susquehanna County    | X        | [Link](https://results.enr.clarityelections.com/PA/Susquehanna/122485/web.345435/#/summary)                                        | CEXML        | X      | Have a pdf too. but its a very weird format.                                                                                               |
| 117  | Tioga County          | X        | [Link](https://www.tiogacountypa.us/departments/voter-registration/election-results)                                               | SPPP         | X      | Has summary pages, actual precincts start at page 5.                                                                                       |
| 119  | Union County          | X        | [Link](https://sites.google.com/unionco.org/unioncoelections/election-information/election-results-by-precinct)                    | Folder       |        | Folder of the same weird format as 115_susquehana                                                                                          |
| 121  | Venango County        | X        | [Link](https://www.venangocountypa.gov/397/Election-Results)                                                                       | SPPP         |        |                                                                                                                                            |
| 123  | Warren County         | X        | [Link](https://warrencountypa.gov/1192/Elections-Voter-Registration)                                                               | UNQ?         |        | Its PICTURES of a blurry SPPP format. JFC.                                                                                                 |
| 125  | Washington County     | X        | [Link](https://www.washingtoncopa.gov/elections/past-election-results)                                                             | SPPP         | X      | Has summary sections.                                                                                                                      |
| 127  | Wayne County          | X        | [Link](https://www.waynecountypa.gov/1006/November-5-2024-Election-Official-Result)                                                | UNQ?         |        | The kind with the wellformed headers/sections?                                                                                             |
| 129  | Westmoreland County   | X        | [Link](https://results.enr.clarityelections.com/PA/Westmoreland/122823/web.345435/#/summary)                                       | CEXML        | X      | It might have write ins                                                                                                                    |
| 131  | Wyoming County        | X        | [Link](https://wyomingcountypa.gov/elections/results/)                                                                             | UNQ?         |        | Simple, but oof.                                                                                                                           |
| 133  | York County           | X        | [Link](https://results.enr.clarityelections.com/PA/York/122493/web.345435/#/summary)                                               | CEXML        | X      |                                                                                                                                            |