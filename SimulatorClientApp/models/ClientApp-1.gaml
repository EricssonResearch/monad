
model ClientApp

/* Model of Client App */

global skills: [SQLSKILL] {
	
	file bus_img <- image_file("../includes/bus.png");

	int nb_client_init <- 16;
	int weekDay <- 0 ;
	int duration_hour_start <- 1;
	int duration_hour_end <- 10;
	
		//new part
	int get_on_nr <- 0;
	int get_of_nr <- 5;

	//file my_file <- csv_file("../includes/position_name.csv");
	list<string> init_position <- list<string>(csv_file("../includes/position_name.csv"));
	
	//Matrix which keeps regular user info
	matrix<string> regular_user2 <- matrix<string>(csv_file("../includes/Request.csv","&"));
	int mx_index;
	list spname_ls2 <- ['Kungshögarna','Regins väg','Valhalls väg','Huges väg ','Topeliusgatan','Värnlundsgatan','Ferlinsgatan','Heidenstamstorg','Kantorsgatan','Djäknegatan',
							 'Portalgatan','Höganäsgatan','Väderkvarnsgatan','Vaksala torg','Stadshuset','Skolgatan','Götgatan','Ekonomikum','Studentstaden','Rickomberga','Oslogatan',
							 'Reykjaviksgatan','Ekebyhus','Sernanders väg','Flogsta centrum','Flogsta vårdcentral','Ihres väg','Noreens väg','Säves väg '];

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
	path road_rout; //we should assign the road to it
	//file bus_img <- image_file("../includes/bus.png");
	
	/*list<point> m  <-  [{415,50,0},{426,100,0},{435,128,0},{454,165,0},{468,200,0},{482,235,0},{454,300,0},{430,338,0},{403,368,0},{383,405,0},{362,435,0},
							   {344,455,0},{320,485,0},{306,515,0},{285,545,0},{325,587,0},{328,660,0},{313,730,0},{305,783,0},{336,898,0},{390,904,0},{490,883,0},
							   {606,863,0},	{773,863,0},{761,766,0},{660,645,0},{598,523,0},{575,470,0},{549,406,0}];*/
	
	path var0 <-  [{415,50,0},{426,100,0},{435,128,0},{454,165,0},{468,200,0},{482,235,0},{454,300,0},{430,338,0},{403,368,0},{383,405,0},{362,435,0},
							   {344,455,0},{320,485,0},{306,515,0},{285,545,0},{325,587,0},{328,660,0},{313,730,0},{305,783,0},{336,898,0},{390,904,0},{490,883,0},
							   {606,863,0},	{773,863,0},{761,766,0},{660,645,0},{598,523,0},{575,470,0},{549,406,0}] ;
	reflex update{
		

		/*loop h from:0 to: length(list){
			do follow speed: speed path:m[h];
		}*/
		do follow speed: speed path:var0;
		//do wander;
		
	}
	
	 aspect bus_move {
               draw  file(bus_img) at: location size: 30 ;
        }
	
	
}


species client skills: [SQLSKILL] {
	
	int user_name <- rnd(500000) update: rnd(500000);
	float current_time <- machine_time update: machine_time;
	string cur_time_str <- (current_time/1000) as_date "%Y y %M m %D d %h h %m m %s seconds" update: (current_time/1000) as_date "%Y y %M m %D d %h h %m m %s seconds"; 
	int cts_length <- length(cur_time_str) update: length(cur_time_str);
	float st_time_duration <- current_time + (duration_hour_start*3600000);
	float end_time_duration <- current_time + (duration_hour_end*3600000);
	
		
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
	
	//list spname_ls2 <- ['Kungshögarna','Regins väg','Valhalls väg','Huges väg ','Topeliusgatan','Värnlundsgatan','Ferlinsgatan','Heidenstamstorg','Kantorsgatan','Djäknegatan',
	//						 'Portalgatan','Höganäsgatan','Väderkvarnsgatan','Vaksala torg','Stadshuset','Skolgatan','Götgatan','Ekonomikum','Studentstaden','Rickomberga','Oslogatan',
	//						 'Reykjaviksgatan','Ekebyhus','Sernanders väg','Flogsta centrum','Flogsta vårdcentral','Ihres väg','Noreens väg','Säves väg '];
		
	//the action for normal request to calculate start time and end time
	action normal_request{
		
		//Using Gauss distribution to simulate rush time for start time , either in moring or in afternoon
			//Calculate Tomorrow's start time 00:00
		today_cur_sec <- float(hour) * 60 * 60 + float(minute) * 60 + float(second);
		tom_start_time <- current_time - today_cur_sec * 1000 + a_day_in_ms;
		//write current_time;
		//write tom_start_time;
		
		//condition
		if mor_aft_rnd = 0 {
			rush_time <- tom_start_time + mor_rush;
		} else if mor_aft_rnd = 1{
			rush_time <- tom_start_time + aft_rush;
		}
		
			
		st_time <- gauss (rush_time, 5000000);
		start_time_str <- (st_time/1000) as_date "%Y y %M m %D d %h h %m m %s seconds";
						
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
			

	
		if st_end_rnd = 0{
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
		
	
	/* Executed every cycle to update start_time and request_time */
	reflex update_att when: weekDay = 1 { 
		
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
			

			
		//if the request come from a reqular user
		if user_name = regular_user2[0,mx_index] {
			//check if start time is null in his/her previuse requests
			if (regular_user2[1,mx_index] = "null"){
				up_to_date_stTime <- "null";
				//The date of new endTime should get update
				
				
				/*if ( hour + mmm> 0){
					string request_time_Date <- copy_between(request_time,0,10) + 1;
					float day_after_request_time <- request_time - today_cur_sec * 1000 + a_day_in_ms;
					
				}else {
					 string request_time_Date <- copy_between(request_time,0,10);
				}*/
				string request_time_Date <- copy_between(request_time,0,10);
				string reg_end_time <-copy_between(regular_user2[2,mx_index],10,16);
				up_to_date_edTime <- request_time_Date + reg_end_time;
			}else {
				up_to_date_edTime <- "null";
				string request_time_Date <- copy_between(request_time,0,10);
				string reg_start_time <-copy_between(regular_user2[1,mx_index],10,16);
				up_to_date_stTime <- request_time_Date + reg_start_time;
			}
	
			save ["userId=" + user_name + "&" + up_to_date_stTime + "&" + up_to_date_edTime + "&" + request_time  + "&stPosition=" + regular_user2[3,mx_index] + "&edPosition=" + regular_user2[4,mx_index] + "&priority=" + priority + "&startPositionLatitude=59.8581" +"&startPositionLongitude=17.6447"] 
		    		to: "ClientRequest" type:csv;
		    		write up_to_date_stTime;

		}else{ //here we need to calculate the startTime and eduration_hour_startndTime based on request time(NORMAL)
			
		
			//Normal Distribution to define hot bus_stops for start position		 
			float hot_stop_weight_st <- gauss(5,1);
	   		int hot_stop_st <- int(hot_stop_weight_st); 
	    	
			//Retrieve hot bus_stop for start position from database
	
			list<list> spname_ls <- list<list> (self select(params:PARAMS, 
                                	select:"SELECT stopName FROM station where stopWeight = " + hot_stop_st));
           
            list<list> spname_ls2 <- list<list> (self select(params:PARAMS, 
                                	select:"SELECT stopName FROM station"));
                                	                				
		    int hot_st_lgt <- length(spname_ls[2]);

			//Normal Distribution to define hot bus_stops for End position
			float hot_stop_weight_ed <- gauss(5,1);
			int hot_stop_ed <- int(hot_stop_weight_ed);

			//Retrieve hot bus_stop for End position from database     
			list<list> spname_ed_ls <- list<list> (self select(params:PARAMS, 
                                	select:"SELECT stopName FROM station where stopWeight = " + hot_stop_ed)); 		       
 
                                	
                                			       
			int hot_ed_lgt <- length(spname_ed_ls[2]);

			//Condition to avoid empty list from database
			//choose a random hot bus_stop from list
							
			if (hot_st_lgt != 0 and hot_ed_lgt !=0){
				start_position <- string(spname_ls[2][rnd(hot_st_lgt-1)][0]);
            	end_position <- string(spname_ed_ls[2][rnd(hot_ed_lgt-1)][0]); 
            	
				do normal_request;
				if passenger_cal_flag = 1 {
					loop i from: 0 to: length(bus_stop_list) - 1{
    	           	 	if (start_position = bus_stop_list[i][0]){
        	       	 		bus_stop_list[i][1] <- int(bus_stop_list[i][1]) + 1 ;
            	   	 		//write 'nr of get_on' +  bus_stop_list[i][0] +  '=' + bus_stop_list[i][1];
               		 	}	
               	 		if (end_position = bus_stop_list[i][0]){
               	 			bus_stop_list[i][2] <- int(bus_stop_list[i][2]) + 1 ;
	               	 		//write 'nr of get_off' +  bus_stop_list[i][0] +  '=' + bus_stop_list[i][2];               	 		
    	           	 	}
        	       	}	
               	}
               	write bus_stop_list;				
				save ["userId=" + user_name + "&" + start_time + "&" + end_time + "&" + request_time  + "&stPosition=" + start_position + "&edPosition=" + end_position + "&priority=" + priority +"&startPositionLatitude=59.8581" +"&startPositionLongitude=17.6447"]
		    			to: "ClientRequest" type:csv;}
		    			   	 
	}}

		
	/* Executed every cycle to update start_time and request_time EVERY WEEKEND */	
	reflex update_att1 when: weekDay = 2{ 
		
			nb_client_init <- 8;
			do priority;
		
			mor_rush <- (9.5 * 60 * 60 * 1000);
			aft_rush <- (15.5 * 60 * 60 * 1000);
		

			request_time <- string(1970 + int(year) - 1)  + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second;
		
			
			//if the request come from a reqular user
			if user_name = regular_user2[0,mx_index] {	
				
				//check if start time is null in his/her previuse requests
				if (regular_user2[1,mx_index] = "null"){
					
					up_to_date_stTime <- "null";
					//The date of new endTime should get update
					string request_time_Date <- copy_between(request_time,0,10);
					string reg_end_time <-copy_between(regular_user2[2,mx_index],10,16);
					up_to_date_edTime <- request_time_Date + reg_end_time;
				}else {
					up_to_date_edTime <- "null";
				}
	
				save ["userId=" + user_name + "&" + up_to_date_stTime + "&" + up_to_date_edTime + "&" + request_time  + "&stPosition=" + regular_user2[3,mx_index] + "&edPosition=" + regular_user2[4,mx_index] + "&priority=" + priority+"&startPositionLatitude=59.8581" +"&startPositionLongitude=17.6447"] 
		    			to: "ClientRequest" type:csv;
		    			write "Oh! we find one reqular user.";

			}else{
				
				mor_rush <- (7.5 * 60 * 60 * 1000);
			 	aft_rush <- (16.5 * 60 * 60 * 1000);
				
				//Normal Distribution to define hot bus_stops for start position		 
				float hot_stop_weight_st <- gauss(3,1);
	    		int hot_stop_st <- int(hot_stop_weight_st); 

				//Retrieve hot bus_stop for start position from database
				
				list<list> spname_ls <- list<list> (self select(params:PARAMS, 
                                	select:"SELECT stopName FROM station where stopWeight = " + hot_stop_st)); 
		                                
       		 	int hot_st_lgt <- length(spname_ls[2]);

				//Normal Distribution to define hot bus_stops for End position
				float hot_stop_weight_ed <- gauss(3,1);
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
					do normal_request;
					if passenger_cal_flag = 1 {
						loop i from: 0 to: length(bus_stop_list) - 1{
    	    	       	 	if (start_position = bus_stop_list[i][0]){
        	    	   	 		bus_stop_list[i][1] <- int(bus_stop_list[i][1]) + 1 ;
            	   		 		//write 'nr of get_on' +  bus_stop_list[i][0] +  '=' + bus_stop_list[i][1];
               		 		}	
	               	 		if (end_position = bus_stop_list[i][0]){
    	           	 			bus_stop_list[i][2] <- int(bus_stop_list[i][2]) + 1 ;
	    	           	 		//write 'nr of get_off' +  bus_stop_list[i][0] +  '=' + bus_stop_list[i][2];               	 		
    	    	       	 	}
        	    	   	}	
	               	}
    	           	write bus_stop_list;
			
					save ["userId=" + user_name + "&" + start_time + "&" + end_time + "&" + request_time  + "&stPosition=" + start_position + "&edPosition=" + end_position + "&priority=" + priority+"&startPositionLatitude=59.8581" +"&startPositionLongitude=17.6447"] 
		    				to: "ClientRequest" type:csv;}
	
		}}

		
	aspect base {
	
		list list_cordinate <-[{415,50,0},{426,100,0},{435,128,0},{454,165,0},{468,200,0},{482,235,0},{454,300,0},{430,338,0},{403,368,0},{383,405,0},{362,435,0},
							   {344,455,0},{320,485,0},{306,515,0},{285,545,0},{325,587,0},{328,660,0},{313,730,0},{305,783,0},{336,898,0},{390,904,0},{490,883,0},
							   {606,863,0},	{773,863,0},{761,766,0},{660,645,0},{598,523,0},{575,470,0},{549,406,0}];
		list list_string_cordinate <-[{415,50,0},{426,100,0},{425,128,0},{454,155,0},{468,208,0},{482,230,0},{454,300,0},{430,338,0},{398,364,0},{383,400,0},{357,430,0},
							   {344,455,0},{310,480,0},{296,510,0},{275,545,0},{325,587,0},{328,660,0},{313,730,0},{305,783,0},{336,898,0},{390,904,0},{490,883,0},
							   {606,863,0},	{773,863,0},{761,766,0},{660,645,0},{598,523,0},{575,470,0},{549,406,0}];
		loop index_cor from: 0 to: length (list_cordinate) - 1 {
			draw circle(6) border:#green size:2 at:list_cordinate[index_cor];
				//loop i from: 0 to: length(bus_stop_list) - 1{
					draw  string(spname_ls2[index_cor]) + ";" + string(bus_stop_list[index_cor][1]) + ":" +string(bus_stop_list[index_cor][1]) color: #blue size:5 at:list_string_cordinate[index_cor];
				//}
		}
		
	}
} 


experiment ClientApp type: gui {
	parameter "Shapefile for the buildings:" var: shape_file_buildings category: "GIS" ;
	parameter "Initial number of clients: " var: nb_client_init min: 1 max: 300 category: "client" ;
	parameter "WeekDay: 1 , weekEnd: 2 " var: weekDay  min: 1 max: 2 category: "Calender" ;
	parameter "Hours start From now " var: duration_hour_start  min: 1 max: 72 category: "Time-screen" ;
	parameter "Hours end From now " var: duration_hour_end  min: 1 max: 72 category: "Time-screen" ;
 	parameter "Shapefile for the roads:" var: shape_file_roads category: "GIS" ;
 	parameter "Shapefile for the bounds:" var: shape_file_bounds category: "GIS";


	output {
		display main_display {
			species client aspect: base;
			 species road aspect: base ;
			 species building aspect: base ;
			 species bus aspect: bus_move;
			 
			
		}

		//Or output file using following code
		//file name: "ClientRequest" type: text data: string(time) refresh_every: 2;	
	}
}
