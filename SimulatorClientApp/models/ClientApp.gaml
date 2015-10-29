
model ClientApp

/* Model of Client App */

global skills: [SQLSKILL] {

	int nb_client_init <- 16;
	

	//connect to server 
	map<string, string> PARAMS <- [
	'host'::'130.238.15.114',
	'dbtype'::'MySQL',
	'database'::'test', // it may be a null string
	'port'::'3306',
	'user'::'testy',
	'passwd'::'testy'];	
	
	
	init {
		create client number: nb_client_init ;
		
		// Test server
		if (self testConnection (params: PARAMS) = true){
			write "Connection is OK" ;
			}else{
			write "Connection is false" ;
		}
	
	
	}
}

species client skills: [SQLSKILL,communicating] {
	
	int user_name <- rnd(500000) update: rnd(500000);
	float current_time <- machine_time update: machine_time;
	string cur_time_str <- (current_time/1000) as_date "%Y y %M m %D d %h h %m m %s seconds" update: (current_time/1000) as_date "%Y y %M m %D d %h h %m m %s seconds"; 
	int cts_length <- length(cur_time_str) update: length(cur_time_str);
	
	float st_time;
	int st_end_rnd <- rnd(1) update: rnd(1);
	string start_time_str;
	int priority_rnd <- rnd(1) update: rnd(1);
	string priority;
	
	/*
	Define variables for caculating rush time.
	Assume client alwasy send request for tomorrow's travel.
	We follow UL's rush hour, it's 6-9 in morning(peak at 7:30) and 3-6 in afternoon(peak at 16:30)
	Using Gauss distribution to simulate rush time.
	We random pick one from morning and afternoon
	*/
	
	float tom_start_time;
	float today_cur_sec;
	float rush_time;
	int mor_aft_rnd <- rnd(1) update: rnd(1);
	float a_day_in_ms <- (24.0 * 60 * 60 * 1000);
	float mor_rush <- (7.5 * 60 * 60 * 1000);
	float aft_rush <- (16.5 * 60 * 60 * 1000);
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
	
	
	string request_time;
	string start_time;
	string end_time;
	
	
	string start_position;
	string end_position;
	
	
	/* Executed every cycle to update start_time and request_time */
	reflex update_att { 
		
		if priority_rnd = 0 {
			priority <- "distance";
		} else {
			priority <- "time";
		}
		
		//Normal Distribution to define hot bus_stops for start position		 
		float hot_stop_weight_st <- gauss(5,1);
	    	int hot_stop_st <- int(hot_stop_weight_st); 

		//Retrieve hot bus_stop for start position from database
		list<list> spname_ls <- list<list> (self select(params:PARAMS, 
                                select:"SELECT stopName FROM station where stopWeight = " + hot_stop_st)); 
		                                
       		 int hot_st_lgt <- length(spname_ls[2]);

		//Normal Distribution to define hot bus_stops for End position
		float hot_stop_weight_ed <- gauss(5,1);
		int hot_stop_ed <- int(hot_stop_weight_ed);

		//Retrieve hot bus_stop for End position from database     
		list<list> spname_ed_ls <- list<list> (self select(params:PARAMS, 
                                select:"SELECT stopName FROM station where stopWeight = " + hot_stop_ed)); 
		       
		int hot_ed_lgt <- length(spname_ed_ls[2]);

		//Condition to avoid empty list from database
		if (hot_st_lgt != 0 and hot_ed_lgt !=0){ 
			//choose a random hot bus_stop from list
			start_position <- string(spname_ls[2][rnd(hot_st_lgt-1)][0]);
                	end_position <- string(spname_ed_ls[2][rnd(hot_ed_lgt-1)][0]); 
      	
			write  start_position;
			write end_position ;   
        
			//Form request time
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
	
			//Using Gauss distribution to simulate rush time for start time , either in moring or in afternoon
			//Calculate Tomorrow's start time 00:00
			today_cur_sec <- float(hour) * 60 * 60 + float(minute) * 60 + float(second);
			tom_start_time <- current_time - today_cur_sec * 1000 + a_day_in_ms;
		
			//condition
			if mor_aft_rnd = 0 {
				rush_time <- tom_start_time + mor_rush;
			} else if mor_aft_rnd = 1{
				rush_time <- tom_start_time + aft_rush;
			}
		
			
			st_time <- gauss (rush_time, 5000000);
			start_time_str <- (st_time/1000) as_date "%Y y %M m %D d %h h %m m %s seconds";
						
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
	

			request_time <- string(1970 + int(year) - 1)  + "-" + month + "-" + day + " " + hour + ":" + minute;
			if st_end_rnd = 0{
				start_time <- string(1970 + int(st_year) - 1)  + "-" + st_month + "-" + st_day + " " + st_hour + ":" + st_minute ;	
				end_time <- "null";
			} else{
				start_time <- "null";
				end_time <- string(1970 + int(st_year) - 1)  + "-" + st_month + "-" + st_day + " " + st_hour + ":" + st_minute;
			}
			

			save ["userId=" + user_name + "&" + start_time + "&" + end_time + "&" + request_time  + "&stPosition=" + start_position + "&edPosition=" + end_position + "&priority=" + priority] 
		    		to: "ClientRequest" type:csv;

		    		
		   ///send to server
		
		
		}}
		
	aspect base {
		draw string(user_name) color: #red size: 3;
	}
} 

experiment ClientApp type: gui {

	parameter "Initial number of clients: " var: nb_client_init min: 1 max: 300 category: "client" ;
	output {
		display main_display {
			species client aspect: base;
		}

		//Or output file using following code
		//file name: "ClientRequest" type: text data: string(time) refresh_every: 2;	
	}
}
