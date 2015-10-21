package se.uu.csproject.monadclient;


import android.os.AsyncTask;
import android.util.Log;

import com.google.common.base.Charsets;

import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.io.DataOutputStream;


public class SendTravelRequest extends AsyncTask<String, Void, String> {
    private static String SERVER = "http://130.238.15.114";

    /* Send the data to the server via POST and receive the response */
    public static String postRequest(String request, String urlParameters) {
        String response = "";

        try {
            URL url = new URL(request);
            byte[] postData = urlParameters.getBytes(Charsets.UTF_8);
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
                throw new RuntimeException("Something went wrong - HTTP error code: " + responseCode);
            }
            BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream())));
            String line;
            while ((line = br.readLine()) != null) {
                response = response + "\n" + line;
            }

            // Close the connection
            conn.disconnect();

        } catch (MalformedURLException e) {
            return ("MalformedURLException: " + e.toString());

        } catch (IOException e) {
            return ("IOException: " + e.toString());

        } catch (RuntimeException e) {
            return (e.toString());
        }

        return response;
    }

    /* Get the data from the interface and wrap them in a request */
    public static String wrapRequest(String username, String startTimeString, String endTimeString,
                                   String requestTimeString, String stPosition, String edPosition) {
        String request = SERVER + "/request";
        SimpleDateFormat df = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
        SimpleDateFormat dfUserInput = new SimpleDateFormat("EEE dd MMM HH:mm");

        Date startTime = null;
        Date endTime = null;
        Date requestTime;

        try {
            if (startTimeString == ""){
                endTime = dfUserInput.parse(endTimeString);
            }else{
                startTime = dfUserInput.parse(startTimeString);
            }
            requestTime = df.parse(requestTimeString);
        } catch (ParseException e) {
            Log.d("oops", e.toString());
            return("Something went wrong with the date formatting");
        }

        String urlParameters = "username=" + username + "&startTime=" + startTime
                + "&endTime=" + endTime + "&requestTime=" + requestTime
                + "&stPosition=" + stPosition + "&edPosition=" + edPosition;
        String response = postRequest(request, urlParameters);

        return response;
    }

    /* This is the function that is called by the button listener */
    @Override
    protected String doInBackground(String... params) {
        String response;

        response = wrapRequest(params[0], params[1], params[2],params[3], params[4], params[5]);

        return response;
    }

    /* Deal with the response returned by the server */
    @Override
    protected void onPostExecute(String response) {
        Log.d("goodJob", response);

        //TODO Stavros: set the scrollview with the response
    }
}


