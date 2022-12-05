try:
	from datetime import datetime
	import pandas as pd
	from platform import python_version

	start_time = datetime.now()

	def scorecard():
		
		dataframe_pakinnings = pd.DataFrame()
		dataframe_indinnings = pd.DataFrame()
		#reading the pak_inns1.tx file/
		try:
			f1=open("india_inns2.txt","r")
			f=open("pak_inns1.txt","r")
			lines=f.readlines()
			#in the lines,it will store each line as a string.  
			f.close()
			result=[]
			#each list will store following lists as a dataframe.
			#presnt_bowl(indicates bowl in this innings)
			present_bowl = []
			#prese_bowelr is a bowler who is bowling right now.
			present_bowler = []
			tos = []
			#prese_batsman is a batter who is batting right now.
			present_batsman = []
			#contents will store what happend in that bowl like 1 run, 2 run, 3run,FOUR,SIX,wide,out..
			contents = []

			for x in lines: 
				if (len(x)>1):
					pres_index = 0
					#here we are storing the the ball of 20overs.
					if (x[3]==' '):
						pres_index = 3
						present_bowl.append(x[0:3])
					else :
						pres_index = 4
						present_bowl.append(x[0:4])
					#storing the present_bowler who is bowling the present bowl.
					for z in range(pres_index+1,len(x)):
						if(x[z]==' ' and x[z+1]=='t' and x[z+2]=='o'):
							present_bowler.append(x[pres_index+1:z])
							pres_index = z
							break
					for z in range(pres_index+1,len(x)):
						if(x[z]==' '):
							tos.append(x[pres_index+1:z])
							pres_index = z
							break	         
					#storing the present_batsman who is bowling the present bowl.
					for z in range(pres_index+1,len(x)):
						if(x[z]==','):
							present_batsman.append(x[pres_index+1:z])
							pres_index = z+1
							break	
					#storing the result of the ball in the contents list.
					for z in range(pres_index+1,len(x)):
						if(x[z]==','):
							contents.append(x[pres_index+1:z])
							pres_index = z
							break	
						elif (x[z]=='!'):
							contents.append(x[pres_index+1:z])
							break

			#creating the columns for the dataframe, storing the commentry part in dataframe.

			dataframe_pakinnings['1st innings bowl'] = present_bowl
			dataframe_pakinnings['2nd innings bowler'] = present_bowler
			dataframe_pakinnings['1st innings batsman'] = present_batsman
			dataframe_pakinnings['result of present_bowl'] = contents

			# print(contents)
			#batters_in_pak stores the batsman in 1st innings from commentry.
			batters_in_pak = sorted(set(present_batsman))
			#bowlers_in_ind stores the batsman in 1st innings from commentry.
			bowlers_in_india = sorted(set(present_bowler))
			#types_of_descrptn stores the unique kind of result in each ball.
			types_of_descptn = sorted(set(contents))

			#here in this following dictonary,i am storing the batsman score,no_of_balls,fours,sixes,bowler who made out batsman,fielder catch.
			individual_score_pakbtrs = {}
			individual_bowls_pakbtrs= {}
			individual_fours_pakbtrs = {}
			individual_sixes_pakbtrs = {}
			bowler_wicket_pakbtrs = {}
			how_wicket_pakbtrs = {}

			#initially i am keeping zero for each batsman's score,bowl,sixes,fours. and not out.
			for i in range(0,len(batters_in_pak)):
				individual_score_pakbtrs[str(batters_in_pak[i])]=0
				individual_bowls_pakbtrs[str(batters_in_pak[i])]=0
				individual_fours_pakbtrs[str(batters_in_pak[i])]=0
				individual_sixes_pakbtrs[str(batters_in_pak[i])]=0
				bowler_wicket_pakbtrs[str(batters_in_pak[i])]='not out'
				how_wicket_pakbtrs[str(batters_in_pak[i])]=''

			#here in this following dictonary,i am storing the bowlers balls,wickets,runs,nbs,wides,maidens of each bowler..
			indian_bowlers_balls = {}
			indian_bowlers_wickets = {}
			indian_bowlers_runs = {}
			indian_bowlers_nbs = {}
			indian_bowlers_wides = {}
			indian_bowlers_maidens = {}
			#total_wides,total_byes stores the no of wides,byes in the 1st innings.
			total_wides = 0
			total_byes = 0

			#initially i am keeping zero for each bowlers, no of balls=0,no of wickets=0,runs=0,nbs=0.wides=0,maidens=0.
			for i in range(0,len(bowlers_in_india)):
				indian_bowlers_balls[bowlers_in_india[i]]=0
				indian_bowlers_wickets[bowlers_in_india[i]]=0
				indian_bowlers_runs[bowlers_in_india[i]]=0
				indian_bowlers_nbs[bowlers_in_india[i]]=0
				indian_bowlers_balls[bowlers_in_india[i]]=0
				indian_bowlers_wides[bowlers_in_india[i]]=0
				indian_bowlers_maidens[bowlers_in_india[i]]=0

			#created a dict mp..which stores the unique types_of_descptn as zero.
			mp = {}
			for i in range(0,len(types_of_descptn)):
				mp[str(types_of_descptn[i])]=0

			#giving a score of each value for different types_of_descptn.
			mp['no run'] = 0
			mp['FOUR'] = 4
			mp['SIX'] = 6
			mp['3 runs'] = 3
			mp['2 runs'] = 2
			mp['1 run'] = 1
			mp['wide'] = 1
			mp['byes'] = 1

			#this types of variables stores the total_score,wickets,overs,power_play_runs in the 1st inninngs.
			total_score = 0
			total_wickets = 0
			total_overs = 0
			power_play_runs = 0

			#in this list, i have stored the wicket of each batsman in the 1st innings. 
			fall_of_wickets = []

			for i in range(0,len(dataframe_pakinnings)):
				#in this dataframe_pakinnings, we traverse through each row..
				#so while traversing the each result in the batsman dict, bowler dict..etc
				if(dataframe_pakinnings['result of present_bowl'][i]=='wide'):
					total_wides+=1
				if(dataframe_pakinnings['result of present_bowl'][i]=='byes'):
					total_byes+=1
				if(dataframe_pakinnings['result of present_bowl'][i][0]=='o'):
					total_wickets+=1
					making_string= ''
					making_string+=(str(total_score))
					making_string+=('-')
					making_string+=(str(total_wickets))
					making_string+=(' (')
					making_string+=(str(dataframe_pakinnings['1st innings batsman'][i]))
					making_string+=(',')
					making_string+=(str(dataframe_pakinnings['1st innings bowl'][i]))
					making_string+=(str(')'))
					fall_of_wickets.append(making_string)
					indian_bowlers_balls[dataframe_pakinnings['2nd innings bowler'][i]]+=1
					indian_bowlers_wickets[dataframe_pakinnings['2nd innings bowler'][i]]+=1
					individual_bowls_pakbtrs[dataframe_pakinnings['1st innings batsman'][i]]+=1
					bowler_wicket_pakbtrs[dataframe_pakinnings['1st innings batsman'][i]] = dataframe_pakinnings['2nd innings bowler'][i]
					if(dataframe_pakinnings['result of present_bowl'][i][4]=='L'):
						how_wicket_pakbtrs[dataframe_pakinnings['1st innings batsman'][i]] = 'lbw '
					elif (dataframe_pakinnings['result of present_bowl'][i][4]=='B'):
						how_wicket_pakbtrs[dataframe_pakinnings['1st innings batsman'][i]] = 'b '
					elif (dataframe_pakinnings['result of present_bowl'][i][4]=='C'):
						how_wicket_pakbtrs[dataframe_pakinnings['1st innings batsman'][i]] = 'c '+str(dataframe_pakinnings['result of present_bowl'][i][14:])+' b '
				else:
					#here i am storing the power_play_runs = 0(as i<=37..so first 6 overs)
					if (i<=37):
						power_play_runs+=mp[dataframe_pakinnings['result of present_bowl'][i]]

					total_score+=mp[dataframe_pakinnings['result of present_bowl'][i]]
					if(dataframe_pakinnings['result of present_bowl'][i]=='FOUR'):
						individual_fours_pakbtrs[dataframe_pakinnings['1st innings batsman'][i]]+=1
					if(dataframe_pakinnings['result of present_bowl'][i]=='SIX'):
						individual_sixes_pakbtrs[dataframe_pakinnings['1st innings batsman'][i]]+=1
					if(dataframe_pakinnings['result of present_bowl'][i]!='wide' and dataframe_pakinnings['result of present_bowl'][i]!='byes'):
						individual_score_pakbtrs[dataframe_pakinnings['1st innings batsman'][i]]+=mp[dataframe_pakinnings['result of present_bowl'][i]]
					if(dataframe_pakinnings['result of present_bowl'][i]!='wide'):
						individual_bowls_pakbtrs[dataframe_pakinnings['1st innings batsman'][i]]+=1
					#for bowlers
					if(dataframe_pakinnings['result of present_bowl'][i]!='wide' and dataframe_pakinnings['result of present_bowl'][i]!='byes'):
						indian_bowlers_balls[dataframe_pakinnings['2nd innings bowler'][i]]+=1
						indian_bowlers_runs[dataframe_pakinnings['2nd innings bowler'][i]]+=mp[dataframe_pakinnings['result of present_bowl'][i]]
					if(dataframe_pakinnings['result of present_bowl'][i]=='wide'):
						indian_bowlers_wides[dataframe_pakinnings['2nd innings bowler'][i]]+=1
						indian_bowlers_runs[dataframe_pakinnings['2nd innings bowler'][i]]+=mp[dataframe_pakinnings['result of present_bowl'][i]]
					if(dataframe_pakinnings['result of present_bowl'][i]=='byes'):
						indian_bowlers_balls[dataframe_pakinnings['2nd innings bowler'][i]]+=1
				if(i%6==5):
					#in this over, i am checking whether the over is maiden or not.
					runs_given = 0
					if(dataframe_pakinnings['result of present_bowl'][i]!='byes'):
						runs_given+=mp[dataframe_pakinnings['result of present_bowl'][i]]
					if(dataframe_pakinnings['result of present_bowl'][i-1]!='byes'):
						runs_given+=mp[dataframe_pakinnings['result of present_bowl'][i-1]]
					if(dataframe_pakinnings['result of present_bowl'][i-2]!='byes'):
						runs_given+=mp[dataframe_pakinnings['result of present_bowl'][i-2]]
					if(dataframe_pakinnings['result of present_bowl'][i-3]!='byes'):
						runs_given+=mp[dataframe_pakinnings['result of present_bowl'][i-3]]
					if(dataframe_pakinnings['result of present_bowl'][i-4]!='byes'):
						runs_given+=mp[dataframe_pakinnings['result of present_bowl'][i-4]]
					if(dataframe_pakinnings['result of present_bowl'][i-5]!='byes'):
						runs_given+=mp[dataframe_pakinnings['result of present_bowl'][i-5]]
					if(runs_given==0):
						indian_bowlers_maidens[dataframe_pakinnings['2nd innings bowler'][i]]+=1
				#in this variable,storing till which over the 1st innings took place.
				total_overs = dataframe_pakinnings['1st innings bowl'][i]



			#NOW INDIA INNINGS!
			#similarly i am calculating in the 2nd innings.

			dataframe_indinnings = pd.DataFrame()

			f1=open("india_inns2.txt","r")
			lines1=f1.readlines()
			f1.close()
			result1=[]
			temp_bowl = []
			temp_bowler = []
			temp_tos = []
			temp_batsman = []
			temp_contents = []


			#similarly like the first innings, here we are storing the each result in a temp_lists.
			for x in lines1:
				if (len(x)>1):
					pres_index1 = 0
					if (x[3]==' '):
						pres_index1 = 3
						temp_bowl.append(x[0:3])
					else :
						pres_index1 = 4
						temp_bowl.append(x[0:4])
					for z in range(pres_index1+1,len(x)):
						if(x[z]==' ' and x[z+1]=='t' and x[z+2]=='o'):
							temp_bowler.append(x[pres_index1+1:z])
							pres_index1 = z
							break
					for z in range(pres_index1+1,len(x)):
						if(x[z]==' '):
							temp_tos.append(x[pres_index1+1:z])
							pres_index1 = z
							break	
					for z in range(pres_index1+1,len(x)):
						if(x[z]==','):
							temp_batsman.append(x[pres_index1+1:z])
							pres_index1 = z+1
							break	
					for z in range(pres_index1+1,len(x)):
						if(x[z]==','):
							if(x[pres_index1+1:z]!='leg byes'):
								temp_contents.append(x[pres_index1+1:z])
								pres_index1 = z
								break	
							else:
								for z1 in range(z+1,len(x)):
									if(x[z1]==','):
										temp_contents.append(x[pres_index1+1:z1])
										pres_index1 = z1
										break	
								break							
						elif (x[z]=='!'):
							temp_contents.append(x[pres_index1+1:z])
							break

			#created the columns same like first innings in this dataframe.
			dataframe_indinnings['over'] = temp_bowl
			dataframe_indinnings['bowler'] = temp_bowler
			dataframe_indinnings['batsman'] = temp_batsman
			dataframe_indinnings['result of present_bowl'] = temp_contents

			#stored the unique kind of batters_in_india,bowlers_in_pak,types_of_descptn1 for the 2nd innings.
			batters_in_india = sorted(set(temp_batsman))
			bowlers_in_pak = sorted(set(temp_bowler))
			types_of_descptn1 = sorted(set(temp_contents))

			#as some of the batsman are not present in the commentry,adding their names manually.
			batters_in_india.append('Bhuvneshwar Kumar')
			batters_in_india.append('Avesh Khan')
			batters_in_india.append('Yuzvendra Chahal')
			batters_in_india.append('Arshdeep Singh')


			#creating diff kind of indbtrs result as score,bowls,fours,sixes,wicket in a dictonary.
			individual_score_indbtrs = {}
			individual_bowls_indbtrs= {}
			individual_fours_indbtrs = {}
			individual_sixes_indbtrs = {}
			bowler_wicket_indbtrs = {}
			how_wicket_indbtrs = {}

			#intially keeping score,bowls,fours,sixes,bowler who too wicket,fielder who took catch in the 2nd innings.
			for i in range(0,len(batters_in_india)):
				individual_score_indbtrs[str(batters_in_india[i])]=0
				individual_bowls_indbtrs[str(batters_in_india[i])]=0
				individual_fours_indbtrs[str(batters_in_india[i])]=0
				individual_sixes_indbtrs[str(batters_in_india[i])]=0
				bowler_wicket_indbtrs[str(batters_in_india[i])]='not out'
				how_wicket_indbtrs[str(batters_in_india[i])]=''

			#similarly storing the diff kinds of possibilities for pak bowlers.
			pakisthan_bowlers_balls = {}
			pakisthan_bowlers_wickets = {}
			pakisthan_bowlers_runs = {}
			pakisthan_bowlers_nbs = {}
			pakisthan_bowlers_wides = {}
			pakisthan_bowlers_maidens = {}

			#Initially keeping the bowlers of pakisthan_bowlers_balls = 0,pakisthan_bowlers_wickets=0,pakisthan_bowlers_runs=0,pakisthan_bowlers_nbs=0..
			for i in range(0,len(bowlers_in_pak)):
				pakisthan_bowlers_balls[bowlers_in_pak[i]]=0
				pakisthan_bowlers_wickets[bowlers_in_pak[i]]=0
				pakisthan_bowlers_runs[bowlers_in_pak[i]]=0
				pakisthan_bowlers_nbs[bowlers_in_pak[i]]=0
				pakisthan_bowlers_balls[bowlers_in_pak[i]]=0
				pakisthan_bowlers_wides[bowlers_in_pak[i]]=0
				pakisthan_bowlers_maidens[bowlers_in_pak[i]]=0

			mp1 = {}
			for i in range(0,len(types_of_descptn1)):
				mp1[str(types_of_descptn1[i])]=0
			#storing the unique kind of result with score.
			mp1['no run'] = 0
			mp1['FOUR'] = 4
			mp1['SIX'] = 6
			mp1['3 runs'] = 3
			mp1['2 runs'] = 2
			mp1['1 run'] = 1
			mp1['wide'] = 1
			mp1['leg byes, FOUR'] = 4
			mp1['leg byes, 1 run'] = 1
			mp1['2 wides'] = 2
			mp1['3 wides'] = 3

			#variables which stores total score,wickets,overs,power_play_runs_ind andkeeping intially 0
			total_score_ind = 0
			total_wickets_ind = 0
			total_overs_ind = 0
			power_play_runs_ind = 0
			fall_of_wickets_ind = []
			total_wides_ind = 0
			total_legbyes_ind = 0
			for i in range(0,len(dataframe_indinnings)):
					#in this dataframe_ininnings, we traverse through each row..
				#so while traversing we store each result in the batsman dict, bowler dict tc
				#this if condition occurs when the batsman gotout inthis ball, reamining all cases he goes to else condition.
				if(dataframe_indinnings['result of present_bowl'][i][0]=='o'):
					total_wickets_ind+=1
					making_string1= ''
					making_string1+=(str(total_score_ind))
					making_string1+=('-')
					making_string1+=(str(total_wickets_ind))
					making_string1+=(' (')
					making_string1+=(str(dataframe_indinnings['batsman'][i]))
					making_string1+=(',')
					making_string1+=(str(dataframe_indinnings['over'][i]))
					making_string1+=(str(')'))
					fall_of_wickets_ind.append(making_string1)
					pakisthan_bowlers_balls[dataframe_indinnings['bowler'][i]]+=1
					pakisthan_bowlers_wickets[dataframe_indinnings['bowler'][i]]+=1
					individual_bowls_indbtrs[dataframe_indinnings['batsman'][i]]+=1
					bowler_wicket_indbtrs[dataframe_indinnings['batsman'][i]] = dataframe_indinnings['bowler'][i]
					if(dataframe_indinnings['result of present_bowl'][i][4]=='L'):
						how_wicket_indbtrs[dataframe_indinnings['batsman'][i]] = 'lbw '
					elif (dataframe_indinnings['result of present_bowl'][i][4]=='B'):
						how_wicket_indbtrs[dataframe_indinnings['batsman'][i]] = 'b '
					elif (dataframe_indinnings['result of present_bowl'][i][4]=='C'):
						how_wicket_indbtrs[dataframe_indinnings['batsman'][i]] = 'c '+str(dataframe_indinnings['result of present_bowl'][i][14:])+' b '
				else:
					#!this is condition is for i<37
					if (i<=37):
						power_play_runs_ind+=mp1[dataframe_indinnings['result of present_bowl'][i]]
					total_score_ind+=mp1[dataframe_indinnings['result of present_bowl'][i]]
					if(dataframe_indinnings['result of present_bowl'][i]=='FOUR'):
						individual_fours_indbtrs[dataframe_indinnings['batsman'][i]]+=1
					if(dataframe_indinnings['result of present_bowl'][i]=='SIX'):
						individual_sixes_indbtrs[dataframe_indinnings['batsman'][i]]+=1
					if(dataframe_indinnings['result of present_bowl'][i]!='wide' and dataframe_indinnings['result of present_bowl'][i]!='leg byes, FOUR' and dataframe_indinnings['result of present_bowl'][i]!='leg byes, 1 run' and dataframe_indinnings['result of present_bowl'][i]!='2 wides' and dataframe_indinnings['result of present_bowl'][i]!='3 wides'):
						individual_score_indbtrs[dataframe_indinnings['batsman'][i]]+=mp1[dataframe_indinnings['result of present_bowl'][i]]
					if(dataframe_indinnings['result of present_bowl'][i]!='wide' and dataframe_indinnings['result of present_bowl'][i]!='2 wides' and dataframe_indinnings['result of present_bowl'][i]!='3 wides'):
						individual_bowls_indbtrs[dataframe_indinnings['batsman'][i]]+=1
					#for bowlers
					if(dataframe_indinnings['result of present_bowl'][i]!='wide'  and dataframe_indinnings['result of present_bowl'][i]!='2 wides' and dataframe_indinnings['result of present_bowl'][i]!='3 wides' and dataframe_indinnings['result of present_bowl'][i]!='leg byes, FOUR' and dataframe_indinnings['result of present_bowl'][i]!='leg byes, 1 run'):
						pakisthan_bowlers_balls[dataframe_indinnings['bowler'][i]]+=1
						pakisthan_bowlers_runs[dataframe_indinnings['bowler'][i]]+=mp1[dataframe_indinnings['result of present_bowl'][i]]
					if(dataframe_indinnings['result of present_bowl'][i]=='leg byes, FOUR' or dataframe_indinnings['result of present_bowl'][i]=='leg byes, 1 run'):
						pakisthan_bowlers_balls[dataframe_indinnings['bowler'][i]]+=1
					if(dataframe_indinnings['result of present_bowl'][i]=='wide' or dataframe_indinnings['result of present_bowl'][i]=='2 wides' or dataframe_indinnings['result of present_bowl'][i]=='3 wides'):
						pakisthan_bowlers_wides[dataframe_indinnings['bowler'][i]]+=mp1[dataframe_indinnings['result of present_bowl'][i]]
						pakisthan_bowlers_runs[dataframe_indinnings['bowler'][i]]+=mp1[dataframe_indinnings['result of present_bowl'][i]]
					if(dataframe_indinnings['result of present_bowl'][i]=='wide' or dataframe_indinnings['result of present_bowl'][i]=='2 wides' or dataframe_indinnings['result of present_bowl'][i]=='3 wides'):
						total_wides_ind+=mp1[dataframe_indinnings['result of present_bowl'][i]]
					if(dataframe_indinnings['result of present_bowl'][i]=='leg byes, FOUR' or dataframe_indinnings['result of present_bowl'][i]=='leg byes, 1 run'):
						total_legbyes_ind+=mp1[dataframe_indinnings['result of present_bowl'][i]]
				if(i%6==5):
					#
					runs_given = 0
					if(dataframe_indinnings['result of present_bowl'][i]!='leg byes, FOUR' and dataframe_indinnings['result of present_bowl'][i]!='leg byes, 1 run'):
						runs_given+=mp1[dataframe_indinnings['result of present_bowl'][i]]
					if(dataframe_indinnings['result of present_bowl'][i-1]!='leg byes, FOUR' and dataframe_indinnings['result of present_bowl'][i]!='leg byes, 1 run'):
						runs_given+=mp1[dataframe_indinnings['result of present_bowl'][i-1]]
					if(dataframe_indinnings['result of present_bowl'][i-2]!='leg byes, FOUR' and dataframe_indinnings['result of present_bowl'][i]!='leg byes, 1 run'):
						runs_given+=mp1[dataframe_indinnings['result of present_bowl'][i-2]]
					if(dataframe_indinnings['result of present_bowl'][i-3]!='leg byes, FOUR' and dataframe_indinnings['result of present_bowl'][i]!='leg byes, 1 run'):
						runs_given+=mp1[dataframe_indinnings['result of present_bowl'][i-3]]
					if(dataframe_indinnings['result of present_bowl'][i-4]!='leg byes, FOUR' and dataframe_indinnings['result of present_bowl'][i]!='leg byes, 1 run'):
						runs_given+=mp1[dataframe_indinnings['result of present_bowl'][i-4]]
					if(dataframe_indinnings['result of present_bowl'][i-5]!='leg byes, FOUR' and dataframe_indinnings['result of present_bowl'][i]!='leg byes, 1 run'):
						runs_given+=mp1[dataframe_indinnings['result of present_bowl'][i-5]]
					if(runs_given==0):
						pakisthan_bowlers_maidens[dataframe_indinnings['bowler'][i]]+=1

				total_overs_ind = dataframe_indinnings['over'][i]
			try:
				file1 = open("Scorecard.txt","w")

				#1st innings results storing in the scorecard.txt, using write function by entering the data which collected above.
				file1.write(f"{'India won by 5 wickets'}\n")
				file1.write("\n")
				#writing the total_score,total_overs in the 1st innings.
				file1.write(f"{'Pakistan Innings': <80}{str(total_score)+'-'+str(total_wickets)+'('+str(total_overs)+str(')')}\n")
				file1.write("\n")
				#creating the headings for batsman.
				file1.write(f"{'Batter':<60}{'R':<5}{'B':<5}{'4s':<5}{'6s':<5}{'SR':<5}\n")

				#using this orders_batsman, i will store the order of openers,middle ordered batsman,bowlers etc in a order.
				orders_batsman = []
				orders_batsman.append(9)
				orders_batsman.append(1)
				orders_batsman.append(3)
				orders_batsman.append(5)
				orders_batsman.append(6)
				orders_batsman.append(10)
				orders_batsman.append(0)
				orders_batsman.append(7)
				orders_batsman.append(4)
				orders_batsman.append(8)
				orders_batsman.append(2)

				#formatting the output of scorecard.txt according to the cricbuzz score card format.
				#aligning the spaces in the scorecard.txt using syntax: f"{'string':< or > 20}" (alloting space of 20 for the string to the right or left.)
				for i in range(0,len(orders_batsman)):
					length_of_line = 20+len(str(how_wicket_pakbtrs[batters_in_pak[orders_batsman[i]]]))+len(str(bowler_wicket_pakbtrs[batters_in_pak[orders_batsman[i]]])) + len(str(individual_score_pakbtrs[batters_in_pak[orders_batsman[i]]]))
					value = 62-length_of_line
					sample = ''
					for z in range(0,value):
						sample+=' '
					sample2 = '   '
					if(len(str(individual_bowls_pakbtrs[batters_in_pak[orders_batsman[i]]]))==1):
						sample2+=' '
					sample3 = '    '
					sample4 = '   '
					if(i!=0 and i!=1):
						file1.write(f"{batters_in_pak[orders_batsman[i]]:<20}{how_wicket_pakbtrs[batters_in_pak[orders_batsman[i]]]}{bowler_wicket_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample}{individual_score_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample2}{individual_bowls_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample3}{individual_fours_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample3}{individual_sixes_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample4}{round((individual_score_pakbtrs[batters_in_pak[orders_batsman[i]]]/individual_bowls_pakbtrs[batters_in_pak[orders_batsman[i]]])*100,2)}\n")
					elif (i==0):
						file1.write(f"{batters_in_pak[orders_batsman[i]]+' (wk)':<20}{how_wicket_pakbtrs[batters_in_pak[orders_batsman[i]]]}{bowler_wicket_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample}{individual_score_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample2}{individual_bowls_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample3}{individual_fours_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample3}{individual_sixes_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample4}{round((individual_score_pakbtrs[batters_in_pak[orders_batsman[i]]]/individual_bowls_pakbtrs[batters_in_pak[orders_batsman[i]]])*100,2)}\n")		
					elif (i==1):
						file1.write(f"{batters_in_pak[orders_batsman[i]]+' (c)':<20}{how_wicket_pakbtrs[batters_in_pak[orders_batsman[i]]]}{bowler_wicket_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample}{individual_score_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample2}{individual_bowls_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample3}{individual_fours_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample3}{individual_sixes_pakbtrs[batters_in_pak[orders_batsman[i]]]}{sample4}{round((individual_score_pakbtrs[batters_in_pak[orders_batsman[i]]]/individual_bowls_pakbtrs[batters_in_pak[orders_batsman[i]]])*100,2)}\n")
				file1.write(f"{'Extras':<61}{total_byes+total_wides}{'(b '+str(total_byes)+',lb 0,w '+str(total_wides)+',nb 0,p 0)'}\n")
				file1.write(f"{'Total':59}{str(total_score)+'('+'10 '+'wkts, '+str(total_overs)+' Ov)'}\n")
				file1.write("\n")
				file1.write(f"{'Fall of Wickets'}\n")
				for i in range(0,len(fall_of_wickets)):
					if(i!=len(fall_of_wickets)-1):
						file1.write(f"{str(fall_of_wickets[i])}{','}")
					else:
						file1.write(f"{str(fall_of_wickets[i])}\n")
					if(i==int(len(fall_of_wickets)/2)):
						file1.write(f"\n")

				file1.write("\n")
				file1.write(f"{'Bowler':<45}{'O':<6}{'M':<6}{'R':<6}{'W':<6}{'NB':<6}{'WD':<6}{'ECO':<6}\n")

				#orders_bowlers stores the order of bowlers in the innings according to scorecard in cricbuzz.
				orders_bowlers = []
				orders_bowlers.append(2)
				orders_bowlers.append(0)
				orders_bowlers.append(4)
				orders_bowlers.append(1)
				orders_bowlers.append(3)
				orders_bowlers.append(5)

				for i in range(0,len(bowlers_in_india)):
					file1.write(f"{bowlers_in_india[orders_bowlers[i]]:<45}{int(indian_bowlers_balls[bowlers_in_india[orders_bowlers[i]]]/6)+(indian_bowlers_balls[bowlers_in_india[orders_bowlers[i]]]%6)/10:<6}{indian_bowlers_maidens[bowlers_in_india[orders_bowlers[i]]]:<6}{indian_bowlers_runs[bowlers_in_india[orders_bowlers[i]]]:<6}{indian_bowlers_wickets[bowlers_in_india[orders_bowlers[i]]]:<6}{indian_bowlers_nbs[bowlers_in_india[orders_bowlers[i]]]:<6}{indian_bowlers_wides[bowlers_in_india[orders_bowlers[i]]]:<6}{round((indian_bowlers_runs[bowlers_in_india[orders_bowlers[i]]]/indian_bowlers_balls[bowlers_in_india[orders_bowlers[i]]])*6,2)}\n")

				#here writing the powerplay runs in the 1st innings.
				file1.write(f"\n")
				file1.write(f"{'Powerplays':<40}{'Overs':<40}{'Runs':<40}\n")

				file1.write(f"{'Mandatory':<40}{'0.1-6':<42}{power_play_runs}\n")

				file1.write("\n")
				file1.write("\n")
				file1.write("\n")

				#indian innings
				file1.write(f"{'India Innings': <80}{str(total_score_ind)+'-'+str(total_wickets_ind)+'('+str(total_overs_ind)+str(')')}\n")
				file1.write("\n")
				file1.write(f"{'Batter':<60}{'R':<5}{'B':<5}{'4s':<5}{'6s':<5}{'SR':<5}\n")

				orders_batsman_ind = []

				#using this orders_batsman, i will store the order of openers,middle ordered batsman,bowlers etc in a order.
				orders_batsman_ind.append(5)
				orders_batsman_ind.append(4)
				orders_batsman_ind.append(3)
				orders_batsman_ind.append(1)
				orders_batsman_ind.append(6)
				orders_batsman_ind.append(0)
				orders_batsman_ind.append(2)

				for i in range(0,len(orders_batsman_ind)):
					length_of_line = 20+len(str(how_wicket_indbtrs[batters_in_india[orders_batsman_ind[i]]]))+len(str(bowler_wicket_indbtrs[batters_in_india[orders_batsman_ind[i]]])) + len(str(individual_score_indbtrs[batters_in_india[orders_batsman_ind[i]]]))
					value = 62-length_of_line
					sample = ''
					for z in range(0,value):
						sample+=' '
					sample2 = '   '
					if(len(str(individual_bowls_indbtrs[batters_in_india[orders_batsman_ind[i]]]))==1):
						sample2+=' '
					sample3 = '    '
					sample4 = '   '
					if(i!=0 and i!=6):
						file1.write(f"{batters_in_india[orders_batsman_ind[i]]:<20}{how_wicket_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{bowler_wicket_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample}{individual_score_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample2}{individual_bowls_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample3}{individual_fours_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample3}{individual_sixes_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample4}{round((individual_score_indbtrs[batters_in_india[orders_batsman_ind[i]]]/individual_bowls_indbtrs[batters_in_india[orders_batsman_ind[i]]])*100,2)}\n")
					elif (i==0):
						file1.write(f"{batters_in_india[orders_batsman_ind[i]]+' (c)':<20}{how_wicket_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{bowler_wicket_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample}{individual_score_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample2}{individual_bowls_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample3}{individual_fours_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample3}{individual_sixes_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample4}{round((individual_score_indbtrs[batters_in_india[orders_batsman_ind[i]]]/individual_bowls_indbtrs[batters_in_india[orders_batsman_ind[i]]])*100,2)}\n")
					elif (i==6):
						file1.write(f"{batters_in_india[orders_batsman_ind[i]]+' (wk)':<20}{how_wicket_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{bowler_wicket_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample}{individual_score_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample2}{individual_bowls_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample3}{individual_fours_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample3}{individual_sixes_indbtrs[batters_in_india[orders_batsman_ind[i]]]}{sample4}{round((individual_score_indbtrs[batters_in_india[orders_batsman_ind[i]]]/individual_bowls_indbtrs[batters_in_india[orders_batsman_ind[i]]])*100,2)}\n")

				file1.write(f"{'Extras':<60}{total_legbyes_ind+total_wides_ind}{'(b 0,'+'lb '+str(total_legbyes_ind)+',w '+str(total_wides_ind)+',nb 0,p 0)'}\n")
				file1.write(f"{'Total':59}{str(total_score_ind)+'('+str(total_wickets_ind)+' '+'wkts, '+str(total_overs_ind)+' Ov)'}\n")
				file1.write(f"{'Did not Bat':<20}{batters_in_india[7]}{' , '}{batters_in_india[8]}{' , '}{batters_in_india[9]}{' , '}{batters_in_india[10]}")
				file1.write("\n")
				file1.write("\n")
				file1.write(f"{'Fall of Wickets'}\n")

				for i in range(0,len(fall_of_wickets_ind)):
					if(i==len(fall_of_wickets_ind)-1):
						file1.write(f"{str(fall_of_wickets_ind[i])}\n")
					else:
						file1.write(f"{str(fall_of_wickets_ind[i])}{', '}")

				file1.write("\n")
				file1.write(f"{'Bowler':<45}{'O':<6}{'M':<6}{'R':<6}{'W':<6}{'NB':<6}{'WD':<6}{'ECO':<6}\n")

				#orders_bowlers stores the order of bowlers in the innings according to scorecard in cricbuzz.
				order_bowlers_pak = []
				order_bowlers_pak.append(3)
				order_bowlers_pak.append(0)
				order_bowlers_pak.append(1)
				order_bowlers_pak.append(4)
				order_bowlers_pak.append(2)


				for i in range(0,len(order_bowlers_pak)):
					file1.write(f"{bowlers_in_pak[order_bowlers_pak[i]]:<45}{int(pakisthan_bowlers_balls[bowlers_in_pak[order_bowlers_pak[i]]]/6)+(pakisthan_bowlers_balls[bowlers_in_pak[order_bowlers_pak[i]]]%6)/10:<6}{pakisthan_bowlers_maidens[bowlers_in_pak[order_bowlers_pak[i]]]:<6}{pakisthan_bowlers_runs[bowlers_in_pak[order_bowlers_pak[i]]]:<6}{pakisthan_bowlers_wickets[bowlers_in_pak[order_bowlers_pak[i]]]:<6}{pakisthan_bowlers_nbs[bowlers_in_pak[order_bowlers_pak[i]]]:<6}{pakisthan_bowlers_wides[bowlers_in_pak[order_bowlers_pak[i]]]:<6}{round((pakisthan_bowlers_runs[bowlers_in_pak[order_bowlers_pak[i]]]/pakisthan_bowlers_balls[bowlers_in_pak[order_bowlers_pak[i]]])*6,2)}\n")

				file1.write("\n")

				#here writing the powerplay runs in the 2nd innings.
				file1.write(f"{'Powerplays':<40}{'Overs':<40}{'Runs':<40}\n")

				file1.write(f"{'Mandatory':<40}{'0.1-6':<42}{power_play_runs_ind}\n")
			except:
				print("compilations/other erros inside the scorecard function")
		except:
			print("Please check your input files path/any other compilation erros while storing the data of 1st,2nd innings")

	ver = python_version()

	if ver == "3.8.10":
		print("Correct Version Installed")
	else:
		print("Please install 3.8.10. Instruction are temp in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

	scorecard()

	#This shall be the last lines of the code.
	end_time = datetime.now()
	print('Duration of Program Execution: {}'.format(end_time - start_time))

except:
	print("Please install the pandas and try to run code/any other compilations errors")
