
model ClientApp

/* Model of Client App */
global skills: [SQLSKILL] {
	file station_img <- image_file("../includes/station.jpg");
	file bus_img <- image_file("../includes/bus1.png");
	
	
	//Four counters
	int weekday_nor_req_count <- 0;
	int weekend_nor_req_count <- 0;
	int counter_reg_req <- 0;

	int nb_client_init <- 16;
	int weekDay <- 0 ;
	int duration_hour_start <- 1;
	int duration_hour_end <- 72;
	int regular_user_flag <- 0;
	int regular_weekly_user_flag <- 0;	
	
	//counters for the data classify by time range
	int counter_before_morning_rush <- 0;
	int counter_morning_rush <- 0;
	int counter_bet_rushs <- 0;
	int counter_afternoon_rush <- 0;
	int counter_after_afternoon_rush <- 0;
	//counters for the data classify by time range
	//file my_file <- csv_file("../includes/position_name.csv");
	list<string> init_position <- list<string>(csv_file("../includes/position_name.csv"));
	
	//Matrix which keeps regular user info
	matrix<string> regular_user2 <- matrix<string>(csv_file("../includes/Regular_user_info.csv","&"));
	matrix<string> regular_user_weekly <- matrix<string>(csv_file("../includes/Regular_user_info_weekly.csv","&"));
	int mx_index;
	list spname_ls2 <- ['Kungshögarna','Regins väg','Valhalls väg','Huges väg','Topeliusgatan','Värnlundsgatan','Ferlinsgatan','Heidenstamstorg','Kantorsgatan','Djäknegatan',
							 'Portalgatan','Höganäsgatan','Väderkvarnsgatan','Vaksala torg','Stadshuset','Skolgatan','Götgatan','Ekonomikum','Studentstaden','Rickomberga','Oslogatan',
							 'Reykjaviksgatan','Ekebyhus','Sernanders väg','Flogsta centrum','Flogsta vårdcentral','Ihres väg','Noreens väg','Säves väg'];

	list<list> bus_stop_list <- list_with (length(spname_ls2),['', 0, 0]);	
	
	string up_to_date_stTime;
	string up_to_date_edTime;
	
    
	int nr_of_position <- length(init_position);
	
	//files needed for visualisaion part
	file shape_file_roads <- file("../includes/road.shp");
	file shape_file_bounds <- file("../includes/bounds.shp");
	file shape_file_buildings <- file("../includes/building.shp");
	geometry shape <- envelope(shape_file_bounds);
	
		    
	//connect to server 
	map<string, string> PARAMS <- [
	'host'::'130.238.15.114',
	'dbtype'::'MySQL',
	'database'::'test', // it may be a null string
	'port'::'3306',
	'user'::'testy',
	'passwd'::'testy'];	
	
	
	init {
		create bus number: 1;
		create client number: nb_client_init ;
		create road from: shape_file_roads ;
		create building from: shape_file_buildings with: [type::string(read ("NATURE"))] {
			if type="Industrial" {
				color <- #blue ;
				
			}
		} 
		
 		loop i from: 0 to: length(spname_ls2) - 1 { 
			bus_stop_list[i] <- [spname_ls2[i], 0, 0];
 		}	
 		
 		
 				
		// Test server
		if (self testConnection (params: PARAMS) = true){
			write "Connection is OK" ;
			}else{
			write "Connection is false" ;
		}
	
	
	}
}
species road  {
        rgb color <- #green ;
        
        aspect base {
                draw shape color: color ;
        }
}

species building {
	string type; 
	rgb color <- #gray  ;
	aspect base {
		draw shape color: color ;
	}
}

species bus skills: [moving]{
	float speed <- 10.0;	
	list road_path <- [{415,50,0},{426,100,0},{435,128,0},{454,165,0},{468,200,0},{482,235,0},{454,300,0},{430,338,0},{403,368,0},{383,405,0},{362,435,0},
							   {344,455,0},{320,485,0},{306,515,0},{285,545,0},{325,587,0},{328,660,0},{313,730,0},{305,783,0},{336,898,0},{390,904,0},{490,883,0},
							   {606,863,0},	{773,863,0},{761,766,0},{660,645,0},{598,523,0},{575,470,0},{549,406,0}];
							   
	point location<-{415,50,0};	
						   
	reflex update{
		//compulsory start-up meeting for master thesis
		do follow speed: speed path:road_path;
		

	}
	
	 aspect bus_move {
               draw  file(bus_img) at:location size: 50 ;
        }
	
	
}


species client skills: [SQLSKILL] {
	
	int user_name <- rnd(500000) update: rnd(500000);
	float current_time <- machine_time update: machine_time;
	string cur_time_str <- ((current_time/1000) + float(13050000)) as_date "%Y y %M m %D d %h h %m m %s seconds" update: ((current_time/1000) + float(13050000)) as_date "%Y y %M m %D d %h h %m m %s seconds"; 
	int cts_length <- length(cur_time_str) update: length(cur_time_str);
	float st_time_duration <- current_time + (duration_hour_start*3600000);
	float end_time_duration <- current_time + (duration_hour_end*3600000);
	float va_titude <- (rnd(9999))/10000000 update: (rnd(9999))/10000000;
	
	float longitude <- 17.644 + va_titude;
	float latitude <- 59.858 + va_titude;
	int weekday <- mod(((current_time/1000) + float(13050000))/(24 * 60 * 60), 7);
	 //+ 13050000
	int weekday1 <- mod(13.5, 7);
	
		
	float st_time;
	int st_end_rnd <- rnd(4) update: rnd(4);
	string start_time_str;
	int priority_rnd <- rnd(1) update: rnd(1);
	string priority;
	
	/*
	Define variables for caculating rush time.
	Assume client alwasy send request for tomorrow's travel.
	We follow UL's rush hour, it's 6-9 in morning(peak at 7:30) and 3-6 in afternoon(peak at 16:30)
	Using Gauss distribution to simulate steprush time.
	We random pick one from morning and afternoon
	*/
	
	float tom_start_time;
	float today_cur_sec;
	float rush_time;
	int mor_aft_rnd <- rnd(1) update: rnd(1);
	float a_day_in_ms <- (24.0 * 60 * 60 * 1000);
	float mor_rush ;
	float aft_rush ;

	float hot_station;
	int cen_plk_rnd <- rnd(1) update: rnd(1);
		
	//Define variable to form request time and start time
	string year;
	string month;
	string day;
	string hour;
	string minute;
	string second;
	
	string st_year;
	string st_month;
	string st_day;
	string st_hour;
	string st_minute;
	string st_second;

	int ct_y_index;
	int ct_mth_index;
	int ct_d_index;
	int ct_h_index;
	int ct_min_index;
	int ct_sec_index;
	
	int st_y_index;
	int st_mth_index;
	int st_d_index;
	int st_h_index;
	int st_min_index;
	int st_sec_index;

	string request_time;
	string start_time;
	string end_time;
	
	
	string start_position;
	string end_position;
	
	int passenger_cal_flag <- 0;	
	
	int org_st_year;
	int org_st_month;
	int org_st_day;
	int org_st_hour;
	int org_st_min;
	int org_end_year;
	int org_end_month;
	int org_end_day;
	int org_end_hour;
	int org_end_min;
	int new_st_year;
	int new_st_month;
	int new_st_day;
	int new_st_hour;
	int new_st_min;
	int new_end_year;
	int new_end_month;
	int new_end_day;
	int new_end_hour;
	int new_end_min;	
	int	org_req_year;
	int	org_req_month;
	int	org_req_day;
	int	org_req_hour;
	int	org_req_min;	
	int	new_req_year;
	int	new_req_month;
	int	new_req_day;
	int	new_req_hour;
	int	new_req_min;	
	string startPositionLatitude;
	string startPositionLongitude;
	string user_name_str;	
	string org_st_time;
	string org_req_time;	
	string new_st_month_str;
	string new_st_day_str;
	string new_req_month_str;
	string new_req_day_str;
	list<int> user_habit;
	
	//list spname_ls2 <- ['Kungshögarna','Regins väg','Valhalls väg','Huges väg','Topeliusgatan','Värnlundsgatan','Ferlinsgatan','Heidenstamstorg','Kantorsgatan','Djäknegatan',
	//						 'Portalgatan','Höganäsgatan','Väderkvarnsgatan','Vaksala torg','Stadshuset','Skolgatan','Götgatan','Ekonomikum','Studentstaden','Rickomberga','Oslogatan',
	//						 'Reykjaviksgatan','Ekebyhus','Sernanders väg','Flogsta centrum','Flogsta vårdcentral','Ihres väg','Noreens väg','Säves väg'];
		
	//the action for normal request to calculate start time and end time
	
	
	
	action normal_request{
		
		//Using Gauss distribution to simulate rush time for start time , either in moring or in afternoon
			//Calculate Tomorrow's start time 00:00regular_user_weekly
		today_cur_sec <- float(hour) * 60 * 60 + float(minute) * 60 + float(second);
		tom_start_time <- current_time - today_cur_sec * 1000 + a_day_in_ms;		
		if mor_aft_rnd = 0 {
			rush_time <- tom_start_time + mor_rush;
		} else if mor_aft_rnd = 1{
			rush_time <- tom_start_time + aft_rush;
		}
		
			
		st_time <- gauss (rush_time, 7000000);
		start_time_str <- ((st_time/1000) +  13050000) as_date "%Y y %M m %D d %h h %m m %s seconds";
						
		if st_time > st_time_duration and st_time < end_time_duration {
			passenger_cal_flag <- 1;	
		}
				
		//Form start time
		st_y_index <- start_time_str index_of "y";
		st_year <- start_time_str at (st_y_index-3) + start_time_str at (st_y_index-2); 
		st_mth_index <- start_time_str index_of "m";
		st_month <- start_time_str at (st_mth_index - 3) + start_time_str at (st_mth_index - 2);
		if int(st_month) < 10{
			st_month <- '0' + string(int(st_month));
		}
		st_d_index <- start_time_str index_of "d";
		st_day <- start_time_str at (st_d_index - 3) + start_time_str at (st_d_index - 2);
		if int(st_day) < 10{
			st_day <- '0' + string(int(st_day));
		}		
		st_h_index <- start_time_str index_of "h";
		st_hour <- start_time_str at (st_h_index - 3) + start_time_str at (st_h_index - 2);
		if int(st_hour) = 0{
			st_hour <- "00";
		} else if int(st_hour) < 10{
			st_hour <- '0' + string(int(st_hour));
		}		
		st_min_index <- start_time_str last_index_of "m";
		st_minute <- start_time_str at (st_min_index - 3) + start_time_str at (st_min_index - 2);
		if int(st_minute) = 0{
			st_minute <- "00";
		} else if int(st_minute) < 10{
			st_minute <- '0' + string(int(st_minute));
		}				
		st_sec_index <- start_time_str index_of "seconds";
		st_second <- start_time_str at (st_sec_index - 3) + start_time_str at (st_sec_index - 2);
		if int(st_second) = 0{
			st_second <- "00";
		} else if int(st_second) < 10{
			st_second <- '0' + string(int(st_second));
		}	
			

	
		if st_end_rnd > 0{
			start_time <- string(1970 + int(st_year) - 1)  + "-" + st_month + "-" + st_day + " " + st_hour + ":" + st_minute + ":" + st_second;	
			end_time <- "null";
		} else{
			start_time <- "null";
			end_time <- string(1970 + int(st_year) - 1)  + "-" + st_month + "-" + st_day + " " + st_hour + ":" + st_minute + ":" + st_second;
			
		}
	}
	
	action priority{
		
		if priority_rnd = 0 {
			priority <- "distance";
		} else {
			priority <- "time";
		}
	
	}
	
	//regular_request
	action regular_request{
		loop i from: 0 to: (regular_user2.rows - 1) {
			if regular_user2[1,i] = nil or regular_user2[2,i] = nil {
				break;
			}
			if regular_user2[1,i] != 'null' {
				org_st_time <- copy_between(regular_user2[1,i], 11,19);
			} else if regular_user2[2,i] != 'null' {
				org_st_time <- copy_between(regular_user2[2,i], 11,19);
			}

			org_req_time <- copy_between(regular_user2[3,i], 11,19);
			
			if regular_user2[1,i] != 'null' {
				start_time <- string(1970 + int(st_year) - 1)  + "-" + st_month + "-" + st_day + ' ' + org_st_time;
				end_time <- regular_user2[2,i];		
			} else {
				end_time <- string(1970 + int(st_year) - 1)  + "-" + st_month + "-" + st_day + ' ' + org_st_time;
				start_time <- regular_user2[1,i];					
			}

			user_name_str <- regular_user2[0,i];
			request_time <- string(1970 + int(year) - 1)  + "-" + month + "-" + day + ' ' + org_req_time;
			
			start_position <- regular_user2[4,i];
			end_position <- regular_user2[5,i];
			priority <- regular_user2[6,i];
			startPositionLatitude <- regular_user2[7,i];
			startPositionLongitude <- regular_user2[8,i];
			
			save [user_name_str + "&" + start_time + "&" + end_time + "&" + request_time + "&" + start_position + "&"+ end_position + "&"+ priority 
					+ "&" + startPositionLatitude + "&" + startPositionLongitude
			] 
		    				to: "ClientRequest" type:csv;
		    				
		    if int(st_hour) < 6  {
		    	counter_before_morning_rush <- counter_before_morning_rush+ 1;
		    }
		    if int(st_hour) > 5 and int(st_hour) < 10 {
		    	counter_morning_rush <- counter_morning_rush + 1;
		    }
		    if int(st_hour) > 9 and int(st_hour) < 15 {
		    	counter_bet_rushs <- counter_bet_rushs + 1;
		    }
		    if int(st_hour) > 14 and int(st_hour) < 19 {
		    	counter_afternoon_rush <- counter_afternoon_rush + 1;
		    }
		    if int(st_hour) > 18 {
		    	counter_after_afternoon_rush <- counter_after_afternoon_rush + 1;
		    }
		     
		    counter_reg_req <- counter_reg_req + 1;
		}
	}
		
	//regular_request_weekly
	action regular_request_weekly{
		loop i from: 0 to: (regular_user_weekly.rows - 1) {
			if regular_user_weekly[1,i] = nil or regular_user_weekly[2,i] = nil {
				break;
			}
			user_habit <- regular_user_weekly[9,i] split_with ',';			
			
			//To make weekday here same as what it is in python. 0 for Sunday, 6 for Satureday
			if (weekday - 1) in user_habit{
				if regular_user_weekly[1,i] = nil or regular_user_weekly[2,i] = nil {
					write "regular_user_weekly is nil!"; 
					break;
				}
				if regular_user_weekly[1,i] != 'null' {
					org_st_time <- copy_between(regular_user_weekly[1,i], 11,19);
				} else if regular_user_weekly[2,i] != 'null' {
					org_st_time <- copy_between(regular_user_weekly[2,i], 11,19);
				}

				org_req_time <- copy_between(regular_user_weekly[3,i], 11,19);
			
				if regular_user_weekly[1,i] != 'null' {
					start_time <- string(1970 + int(st_year) - 1)  + "-" + st_month + "-" + st_day + ' ' + org_st_time;
					end_time <- regular_user_weekly[2,i];		
				} else {
					end_time <- string(1970 + int(st_year) - 1)  + "-" + st_month + "-" + st_day + ' ' + org_st_time;
					start_time <- regular_user_weekly[1,i];					
				}

				user_name_str <- regular_user_weekly[0,i];
				request_time <- string(1970 + int(year) - 1)  + "-" + month + "-" + day + ' ' + org_req_time;
		
				start_position <- regular_user_weekly[4,i];
				end_position <- regular_user_weekly[5,i];
				priority <- regular_user_weekly[6,i];
				startPositionLatitude <- regular_user_weekly[7,i];
				startPositionLongitude <- regular_user_weekly[8,i];
		
				save [user_name_str + "&" + start_time + "&" + end_time + "&" + request_time + "&" + start_position + "&"+ end_position+ "&" + priority 
						+ "&"+ startPositionLatitude + "&" + startPositionLongitude
				] 
		    					to: "ClientRequest" type:csv;
			}
		}
	}
		
	/* Executed every cycle to update start_time and request_time */
	reflex update_att when: (weekDay = 1) { 
		
		do priority;
		mor_rush <- (7.5 * 60 * 60 * 1000);
		aft_rush <- (16.5 * 60 * 60 * 1000);
		
		//Form request time (BOTH)
		ct_y_index <- cur_time_str index_of "y";
		year <- cur_time_str at (ct_y_index-3) + cur_time_str at (ct_y_index-2); 
		ct_mth_index <- cur_time_str index_of "m";
		month <- cur_time_str at (ct_mth_index - 3) + cur_time_str at (ct_mth_index - 2);
		if int(month) < 10{
			month <- '0' + string(int(month));
		}
		ct_d_index <- cur_time_str index_of "d";
		day <- cur_time_str at (ct_d_index - 3) + cur_time_str at (ct_d_index - 2);
		if int(day) < 10{
			day <- '0' + string(int(day));
		}		
		ct_h_index <- cur_time_str index_of "h";
		hour <- cur_time_str at (ct_h_index - 3) + cur_time_str at (ct_h_index - 2);
		if int(hour) = 0{
			hour <- "00";
		} else if int(hour) < 10{
			hour <- '0' + string(int(hour));
		}		
		ct_min_index <- cur_time_str last_index_of "m";
		minute <- cur_time_str at (ct_min_index - 3) + cur_time_str at (ct_min_index - 2);
		if int(minute) = 0{
			minute <- "00";
		} else if int(minute) < 10{
			minute <- '0' + string(int(minute));
		}				
		ct_sec_index <- cur_time_str index_of "seconds";
		second <- cur_time_str at (ct_sec_index - 3) + cur_time_str at (ct_sec_index - 2);
		if int(second) = 0{
			second <- "00";
		} else if int(second) < 10{
			second <- '0' + string(int(second));
		}	

		request_time <- string(1970 + int(year) - 1)  + "-" + month + "-" + day + " " + hour + ":" + minute+ ":" + second;
		

		//prepare start_time and end_time for both random and regular request
		do normal_request;
			
		//Generate weekly habit user's request
		if regular_weekly_user_flag = 0 {
			do regular_request_weekly;
			regular_weekly_user_flag <- 1;
		}			
		
		//If the request come from a reqular user
		//regular_request
		if regular_user_flag = 0 {
			do regular_request;
			regular_user_flag <- 1;
		}else{ //here we need to calculate the startTime and eduration_hour_startndTime based on request time(NORMAL)
			
		
			//Normal Distribution to define hot bus_stops for start position		 
			float hot_stop_weight_st <- gauss(5,1.5);
	   		int hot_stop_st <- int(hot_stop_weight_st); 
	    	
			//Retrieve hot bus_stop for start position from database
	
			list<list> spname_ls <- list<list> (self select(params:PARAMS, 
                                	select:"SELECT stopName FROM station where active = 1 and stopWeight = " + hot_stop_st));
           
//            list<list> spname_ls2 <- list<list> (self select(params:PARAMS, 
//                                	select:"SELECT stopName FROM station"));
                                	                				
		    int hot_st_lgt <- length(spname_ls[2]);

			//Normal Distribution to define hot bus_stops for End position
			float hot_stop_weight_ed <- gauss(5,1.5);
			int hot_stop_ed <- int(hot_stop_weight_ed);
			
			

			//Retrieve hot bus_stop for End position from database     
			list<list> spname_ed_ls <- list<list> (self select(params:PARAMS, 
                                	select:"SELECT stopName FROM station where active = 1 and stopWeightOff = " + hot_stop_ed)); 		       
 
                                	
                                			       
			int hot_ed_lgt <- length(spname_ed_ls[2]);

			//Condition to avoid empty list from database
			//choose a random hot bus_stop from list
							
			if (hot_st_lgt != 0 and hot_ed_lgt !=0){
				start_position <- string(spname_ls[2][rnd(hot_st_lgt-1)][0]);
            	end_position <- string(spname_ed_ls[2][rnd(hot_ed_lgt-1)][0]); 
            	

				if passenger_cal_flag = 1 {
					loop i from: 0 to: length(bus_stop_list) - 1{
    	           	 	if (start_position = bus_stop_list[i][0]){
        	       	 		bus_stop_list[i][1] <- int(bus_stop_list[i][1]) + 1 ;
            	   	 		
               		 	}	
               	 		if (end_position = bus_stop_list[i][0]){
               	 			bus_stop_list[i][2] <- int(bus_stop_list[i][2]) + 1 ;
	               	 		             	 		
    	           	 	}
        	       	}	
               	}	             	
               				
				save ["userId=" + user_name + "&" + start_time + "&" + end_time + "&" + request_time  + "&stPosition=" + start_position + 
				"&edPosition=" + end_position + "&priority=" + priority +"&startPositionLatitude="+latitude +"&startPositionLongitude="+longitude]
		    			to: "ClientRequest" type:csv;}
		   		
		   		if int(st_hour) < 6  {
		    	counter_before_morning_rush <- counter_before_morning_rush+ 1;
		   	    }
		    	if int(st_hour) > 5 and int(st_hour) < 10 {
		    	counter_morning_rush <- counter_morning_rush + 1;
		    	}
		   		if int(st_hour) > 9 and int(st_hour) < 15 {
		    	counter_bet_rushs <- counter_bet_rushs + 1;
		    	}
		    	if int(st_hour) > 14 and int(st_hour) < 19 {
		    	counter_afternoon_rush <- counter_afternoon_rush + 1;
		    	}
		    	if int(st_hour) > 18 {
		    	counter_after_afternoon_rush <- counter_after_afternoon_rush + 1;
		    	}
		   		
		    	weekday_nor_req_count <- weekday_nor_req_count + 1;
		    			   	 
	}}

		
	/* Executed every cycle to update start_time and request_time EVERY WEEKEND */	
	reflex update_att1 when: weekDay = 2{ 
		
			nb_client_init <- 8;
			do priority;
		
			mor_rush <- (10.5 * 60 * 60 * 1000);
			aft_rush <- (15.5 * 60 * 60 * 1000);
			
			//Form request time (BOTH)
			ct_y_index <- cur_time_str index_of "y";
			year <- cur_time_str at (ct_y_index-3) + cur_time_str at (ct_y_index-2); 
			ct_mth_index <- cur_time_str index_of "m";
			month <- cur_time_str at (ct_mth_index - 3) + cur_time_str at (ct_mth_index - 2);
			if int(month) < 10{
				month <- '0' + string(int(month));
			}
			ct_d_index <- cur_time_str index_of "d";
			day <- cur_time_str at (ct_d_index - 3) + cur_time_str at (ct_d_index - 2);
			if int(day) < 10{
				day <- '0' + string(int(day));
			}		
			ct_h_index <- cur_time_str index_of "h";
			hour <- cur_time_str at (ct_h_index - 3) + cur_time_str at (ct_h_index - 2);
			if int(hour) = 0{
				hour <- "00";
			} else if int(hour) < 10{
				hour <- '0' + string(int(hour));
			}		
			ct_min_index <- cur_time_str last_index_of "m";
			minute <- cur_time_str at (ct_min_index - 3) + cur_time_str at (ct_min_index - 2);
			if int(minute) = 0{
				minute <- "00";
			} else if int(minute) < 10{
				minute <- '0' + string(int(minute));
			}				
			ct_sec_index <- cur_time_str index_of "seconds";
			second <- cur_time_str at (ct_sec_index - 3) + cur_time_str at (ct_sec_index - 2);
			if int(second) = 0{
				second <- "00";
			} else if int(second) < 10{
				second <- '0' + string(int(second));
			}	
		

			request_time <- string(1970 + int(year) - 1)  + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second;
		
			//prepare start_time and end_time for both random and regular request
			do normal_request;
			
			//Generate weekly habit user's request
			if regular_weekly_user_flag = 0 {
				do regular_request_weekly;
				regular_weekly_user_flag <- 1;
			}				
					
			//if the request come from a reqular user
			//regular_request
			if regular_user_flag = 0 {
				do regular_request;
				regular_user_flag <- 1;
				
			}else{
				
				mor_rush <- (10.5 * 60 * 60 * 1000);
				aft_rush <- (15.5 * 60 * 60 * 1000);
				
				//Normal Distribution to define hot bus_stops for start position		 
				float hot_stop_weight_st <- gauss(3,1);
	    		int hot_stop_st <- int(hot_stop_weight_st); 

				//Retrieve hot bus_stop for start position from database
				
				list<list> spname_ls <- list<list> (self select(params:PARAMS, 
                                	select:"SELECT stopName FROM station where active = 1 and stopWeight = " + hot_stop_st)); 
		                                
       		 	int hot_st_lgt <- length(spname_ls[2]);

				//Normal Distribution to define hot bus_stops for End position
				float hot_stop_weight_ed <- gauss(3,1);
				int hot_stop_ed <- int(hot_stop_weight_ed);

				//Retrieve hot bus_stop for End position from database 
			  
				list<list> spname_ed_ls <- list<list> (self select(params:PARAMS, 
                                		select:"SELECT stopName FROM station where active = 1 and stopWeightOff = " + hot_stop_ed)); 
		       
				int hot_ed_lgt <- length(spname_ed_ls[2]);

				//Condition to avoid empty list from database
				if (hot_st_lgt != 0 and hot_ed_lgt !=0){ 
					//choose a random hot bus_stop from list
					start_position <- string(spname_ls[2][rnd(hot_st_lgt-1)][0]);
              	  	end_position <- string(spname_ed_ls[2][rnd(hot_ed_lgt-1)][0]); 
            
					if passenger_cal_flag = 1 {
						loop i from: 0 to: length(bus_stop_list) - 1{
    	    	       	 	if (start_position = bus_stop_list[i][0]){
        	    	   	 		bus_stop_list[i][1] <- int(bus_stop_list[i][1]) + 1 ;
            	   		 		
               		 		}	
	               	 		if (end_position = bus_stop_list[i][0]){
    	           	 			bus_stop_list[i][2] <- int(bus_stop_list[i][2]) + 1 ;
	    	           	 		             	 		
    	    	       	 	}
        	    	   	}	
	               	}
					save ["userId=" + user_name + "&" + start_time + "&" + end_time + "&" + request_time  + "&stPosition=" + 
						start_position + "&edPosition=" + end_position + "&priority=" + priority+"&startPositionLatitude="+latitude +"&startPositionLongitude="+longitude
					]
					 
		    				to: "ClientRequest" type:csv;}
		    				
		    		if int(st_hour) < 6  {
		    			counter_before_morning_rush <- counter_before_morning_rush+ 1;
		   			}
		    		if int(st_hour) > 5 and int(st_hour) < 10 {
		    			counter_morning_rush <- counter_morning_rush + 1;
		    		}
		    		if int(st_hour) > 9 and int(st_hour) < 15 {
		    			counter_bet_rushs <- counter_bet_rushs + 1;
		    		}
		    		if int(st_hour) > 14 and int(st_hour) < 19 {
		    			counter_afternoon_rush <- counter_afternoon_rush + 1;
		   			}
		    		if int(st_hour) > 18 {
		    			counter_after_afternoon_rush <- counter_after_afternoon_rush + 1;
		    		}
		    				
					weekend_nor_req_count <- weekend_nor_req_count + 1;
		}}

		
	aspect base {
	
		list list_cordinate <-[{415,50,0},{426,100,0},{435,128,0},{454,165,0},{468,200,0},{482,235,0},{454,300,0},{430,338,0},{403,368,0},{383,405,0},{362,435,0},
							   {344,455,0},{320,485,0},{306,515,0},{285,545,0},{325,587,0},{328,660,0},{313,730,0},{305,783,0},{336,898,0},{390,904,0},{490,883,0},
							   {606,863,0},	{773,863,0},{761,766,0},{660,645,0},{598,523,0},{575,470,0},{549,406,0}];
		list list_string_cordinate <-[{415,50,0},{426,100,0},{425,128,0},{454,155,0},{468,208,0},{482,230,0},{454,300,0},{430,338,0},{398,364,0},{383,400,0},{357,430,0},
							   {344,455,0},{310,480,0},{296,510,0},{275,545,0},{325,587,0},{328,660,0},{313,730,0},{305,783,0},{336,898,0},{390,904,0},{490,883,0},
							   {606,863,0},	{773,863,0},{761,766,0},{660,645,0},{598,523,0},{575,470,0},{549,406,0}];
		loop index_cor from: 0 to: length (list_cordinate) - 1 {
			draw  file(station_img) size:20 at:list_cordinate[index_cor];
					draw  string(spname_ls2[index_cor]) + ";" + string(bus_stop_list[index_cor][1]) + ":" 
					+string(bus_stop_list[index_cor][2]) color: #black size:7 at:list_string_cordinate[index_cor];
		}
	}
} 


experiment ClientApp type: gui {
	parameter "Shapefile for the buildings:" var: shape_file_buildings category: "GIS" ;
	parameter "Initial number of clients: " var: nb_client_init min: 1 max: 300 category: "client" ;
	parameter "WeekDay: 1 , weekEnd: 2 " var: weekDay  min: 1 max: 2 category: "Calender" ;
	parameter "Minutes start From now " var: duration_hour_start  min: 0 max: 720 category: "Time-screen" ;
	parameter "Minutes end From now " var: duration_hour_end  min: 1 max: 72 category: "Time-screen" ;
 	parameter "Shapefile for the roads:" var: shape_file_roads category: "GIS" ;
 	parameter "Shapefile for the bounds:" var: shape_file_bounds category: "GIS";


	output {
		display main_display {
			 species road aspect: base;
			 species building aspect: base ;
			 species client aspect: base;
			 species bus aspect: bus_move;	
		}
		display chart_display refresh_every: 1 { 
         	chart "Requsts" type: pie {
            data "Number of normal requests " value: (weekday_nor_req_count + weekend_nor_req_count) style: line color: rgb("green") ;
            data "Number of regular requests " value: counter_reg_req style: line color: rgb("yellow") ;
         	}
      	}
//      	display chart_display2 refresh_every: 1 { 
//         	chart "Requsts" type: scatter {
//            	loop index_cor from: 0 to: length (spname_ls2) - 1 {
//					data "" value: ("df",2);
//					//data "" value: point(spname_ls2[index_cor],bus_stop_list[index_cor][1]);
//		}
//         	}
//      	}
	  display DataDistributionByBusstop refresh_every: 1{
			chart "DataDistributionByBusstop" type:histogram style:"3d"
			{
				//loop index_cor from: 0 to: length (spname_ls2) - 1 {
					//datalist [spname_ls2] value:[bus_stop_list[index_cor][1]] color:[°red];
				//}
				//datalist ["empty","carry"] value:[(list(ant) count (!each.hasFood)),(list(ant) count (each.hasFood))] color:[°red,°green];bus_stop_list[index_cor][2]
				datalist [spname_ls2[0],spname_ls2[12],spname_ls2[18],spname_ls2[5],spname_ls2[13],spname_ls2[14]
					,spname_ls2[25],spname_ls2[9],spname_ls2[10],spname_ls2[26],spname_ls2[28]/*,'11','12',spname_ls2[13],spname_ls2[14],'15','16','17','18','19','20','21'
					,'22','23','24',spname_ls2[25],'26','27','28','29'*/
				] value:[bus_stop_list[0][1],
					bus_stop_list[12][1],bus_stop_list[18][1],bus_stop_list[5][1],bus_stop_list[13][1],
					bus_stop_list[14][1],bus_stop_list[25][1],bus_stop_list[9][1] ,bus_stop_list[10][1],
					bus_stop_list[26][1],bus_stop_list[28][1]] color:[rgb("red")];				
			}
	  }
	  
	  display DataDistributionByTime refresh_every: 1{
			chart "DataDistributionByTime" type:histogram style:"3d"
			{
				datalist ["Befor 6am","Morning rush","9am - 15pm","Afternoon rush","18pm-24pm"] value:[counter_before_morning_rush,counter_morning_rush,counter_bet_rushs,
						counter_afternoon_rush,counter_after_afternoon_rush
				] color:[°red,°green];			
			}
	  }
   }
}
