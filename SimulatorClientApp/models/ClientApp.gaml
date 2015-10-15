/**
 *  ClientApp
 *  Author: tingwei
 *  Description: 
 */

model ClientApp

/* Model of Client App */

global skills: [SQLSKILL] {

	int nb_client_init <- 16;
	
	//Fetch position data from local csv file and put that into a matrix 
	file my_csv_file <- csv_file("../includes/position.csv",",");
	matrix position_mx <- matrix(my_csv_file);

	/* connect to server 
	map<string, string> PARAMS <- [
	'host'::'130.238.15.114',
	'dbtype'::'MySQL',
	'database'::'', // it may be a null string
	'port'::'3306',
	'user'::'test',
	'passwd'::'test'];	
	*/
	
	init {
		create client number: nb_client_init ;
		
		/* Test server
		if (self testConnection (params: PARAMS) = true){
			write "Connection is OK" ;
			}else{
			write "Connection is false" ;
		}
		*/
	}
}

species client skills: [SQLSKILL] {

	int street_amount <- position_mx.rows - 1;
	int stposition_rnd <- rnd(street_amount) update: rnd(street_amount);
	int edposition_rnd <- rnd(street_amount) update: rnd(street_amount);
	string start_position <- string(position_mx [1, stposition_rnd]) update: string(position_mx [1, stposition_rnd]);
	string end_position <- string(position_mx [1, edposition_rnd]) update: string(position_mx [1, edposition_rnd]);
	string user_feedback;
	
	int user_name <- rnd(500000) update: rnd(500000);
	float current_time <- machine_time update: machine_time;
	string cur_time_str <- (current_time/1000) as_date "%Y y %M m %D d %h h %m m %s seconds" update: (current_time/1000) as_date "%Y y %M m %D d %h h %m m %s seconds"; 
	int cts_length <- length(cur_time_str) update: length(cur_time_str);

	int time_interval <- rnd(10800000) update: rnd(10800000);
	float st_time <- machine_time + time_interval update: machine_time + time_interval;
	string start_time_str <- (st_time/1000) as_date "%Y y %M m %D d %h h %m m %s seconds" update: (st_time/1000) as_date "%Y y %M m %D d %h h %m m %s seconds"; 
	int sts_length <- length(start_time_str) update: length(start_time_str);
	
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
	
	/* Executed every cycle to update start_time and request_time */
	reflex update_att { 
		
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

		request_time <- string(1970 + int(year) - 1)  + "-" + month + "-" + day + "," + hour + ":" + minute + ":" + second;
		start_time <- string(1970 + int(st_year) - 1)  + "-" + st_month + "-" + st_day + "," + st_hour + ":" + st_minute + ":" + st_second;
		save ["username = " + user_name + "; RequestTime = " + request_time + "; StartTime = " + start_time + "; StartPosition = " + start_position + "; EndPosition = " + end_position] 
		     to: "ClientRequest" type:text;

	}
		
	aspect base {
		draw string(user_name) color: #red size: 3;
	}
} 

experiment ClientApp type: gui {

	parameter "Initial number of clients: " var: nb_client_init min: 1 max: 300 category: "client" ;
	output {
		display main_display {
			species client aspect: base ;
		}

		//Or output file using following code
		//file name: "ClientRequest" type: text data: string(time) refresh_every: 2;	
	}
}
