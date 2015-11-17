
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.text.DateFormat;

import java.nio.charset.StandardCharsets;
import java.io.DataOutputStream;


class csvReader{

private static String SERVER = "http://130.238.15.114:2001";

	public static void main(String [ ] args)
	{	
   		readCsvFile();
	}

	public static void readCsvFile(){

		BufferedReader fileReader = null;
		
	    try {
		
		/*Create a new list of request to be filled by txt file*/
		

		String line = "";
		String txtSplitBy = "&";
	

		/*Read the file*/		
		fileReader = new BufferedReader(new FileReader("ClientRequest.txt"));	

		/*Read the file line by line*/
		while ((line = fileReader.readLine()) != null) {
			/*To put each line in an array splited by "&" */
			String[] request = line.split(txtSplitBy);

			/*Change format of the time*/
			DateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
			DateFormat requestFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		
			if (request[1].contains("null")){
				request[1] = "startTime=null";
				String edTime= request[2];
				String endT = requestFormat.format(df.parse(edTime));
				request[2] = "endTime=" + endT;
			} else {
				request[2] = "endTime=null";
				String stTime = request[1];
				Date d1 = df.parse(stTime);
				String stT = requestFormat.format(df.parse(stTime));
				request[1] = "startTime=" + stT;
			}

			String reqTime = request[3];
			Date d3 = df.parse(reqTime);
			String reqT = requestFormat.format(df.parse(reqTime));
			request[3] = "requestTime=" + reqT;
			
	
			System.out.println(request[0]+ "&" +request[1]+ "&" + request[2]+ "&"+request[3]+ "&"+ request[4]+ "&" 
				+ request[5] + "&" + request[6] + "&" + request[7] +"&" + request[8]);
		
			String urlparams = request[0]+ "&" +request[1]+ "&" + request[2]+ "&"+request[3]+ "&"+ request[4]+ "&" 
				+ request[5] + "&" + request[6] + "&" + request[7]+"&" + request[8];
			Thread.sleep(200);
			doInBackground(urlparams);
		}

	    }
		
	    catch (Exception e){
	    	System.out.println("Error in CsvFileReader !");
		e.printStackTrace();
	    } finally {
	      	try {
	      	    fileReader.close();
	      	} catch (IOException e) {
		    System.out.println("Error while closing fileReader !");
		    e.printStackTrace();
		  }
	      }

	}



	    /* Send the data to the server via POST and receive the response */
	    public static String postRequest(String request, String urlParameters) {
		String response = "";

        try {
            URL url = new URL(request);
            byte[] postData = urlParameters.getBytes(StandardCharsets.UTF_8);
            int postDataLength = postData.length;

            // Setup connection to the server
            HttpURLConnection conn = (HttpURLConnection)url.openConnection();
            conn.setDoOutput(true);
            conn.setInstanceFollowRedirects(false);
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            conn.setRequestProperty("charset", "utf-8");
            conn.setRequestProperty("Content-Length", Integer.toString(postDataLength));
            conn.setUseCaches(false);

            // Send the data
            DataOutputStream outputStream = new DataOutputStream(conn.getOutputStream());
            outputStream.write(postData);

            // Get the response from the server
            int responseCode = conn.getResponseCode();
            if (responseCode != 200 && responseCode != 500 && responseCode != 403) {
            	System.out.println("Something is wrong here!!!");
                throw new RuntimeException("Something went wrong - HTTP error code: " + responseCode);
            }
           

            // Close the connection
            conn.disconnect();

        } catch (MalformedURLException e) {
        	System.out.println("Something is wrong here!!!");
            return ("MalformedURLException: " + e.toString());

        } catch (IOException e) {
        	System.out.println("Something is wrong here!!!");
            return ("IOException: " + e.toString());

        } catch (RuntimeException e) {
        	System.out.println("Something is wrong here!!!");
            return (e.toString());
        }

        return response;
    }

    /* Get the data from the interface and wrap them in a request 
    public static String wrapRequest(String userId, String startTime, String endTime,
                                   String requestTime, String stPosition, String edPosition, String priority) {
        String request = SERVER + "/request";

        String urlParameters = "userId=" + userId + "&startTime=" + startTime
                + "&endTime=" + endTime + "&requestTime=" + requestTime
                + "&stPosition=" + stPosition + "&edPosition=" + edPosition
                + "&priority=" + priority;
        String response = postRequest(request, urlParameters);

        return response;
    } */

    /* This is the function that is called by the button listener */
    
    protected static void doInBackground(String params) {
		String request = SERVER + "/request";
        postRequest(request,params);
    }

}
	
	
 
