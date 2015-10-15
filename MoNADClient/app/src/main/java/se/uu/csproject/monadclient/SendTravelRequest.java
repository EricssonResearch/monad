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
import java.text.SimpleDateFormat;
import java.util.Date;
import java.io.DataOutputStream;



public class SendTravelRequest extends AsyncTask<String, Void, String> {
    private static String SERVER;
    private static boolean sendOutSuccessful =false;

    /* Post the request and get the response from the server */
    public static String postRequest(String request, String urlParameters) {
        String response = "";

        try {
            URL url = new URL(request);
            byte[] postData = urlParameters.getBytes(Charsets.UTF_8);
            int postDataLength = postData.length;

            // Setup connection
            HttpURLConnection conn= (HttpURLConnection) url.openConnection();
            conn.setDoOutput(true);
            conn.setInstanceFollowRedirects(false);
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            conn.setRequestProperty("charset", "utf-8");
            conn.setRequestProperty("Content-Length", Integer.toString(postDataLength));
            conn.setUseCaches(false);


            // Post request data
            DataOutputStream outputStream = new DataOutputStream(conn.getOutputStream());
            outputStream.write(postData);

            // Show response from the server
            if (conn.getResponseCode() != 200) {
                throw new RuntimeException("Failed : HTTP error code : "
                        + conn.getResponseCode());
            }
            BufferedReader br = new BufferedReader(new InputStreamReader(
                    (conn.getInputStream())));

            String line;

            while ((line = br.readLine()) != null) {
                response = response + "\n" + line;
            }

            sendOutSuccessful = true;
            conn.disconnect();

        } catch (MalformedURLException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();

        } catch (RuntimeException e) {
            e.printStackTrace();
        }
        return response;
    }

    /* Get the data from the interface and wrap them in a request */
    public static String wrapRequest(String username, Date startTime, Date endTime,
                                   Date requestTime, String stPosition, String edPosition) {
        SERVER = "http://130.238.15.114";
        String request = SERVER + "/request";
        SimpleDateFormat dateFormatter = new SimpleDateFormat("E yyyy.MM.dd 'at' hh:mm:ss");
        String urlParameters = "username=" + username + "&startTime=" + dateFormatter.format(startTime)
                + "&endTime=" + dateFormatter.format(endTime) + "&requestTime=" + dateFormatter.format(requestTime)
                + "&stPosition=" + stPosition + "&edPosition=" + edPosition;
        String response = postRequest(request, urlParameters);

        // record the response from the server
        Log.i("successful :", "\nOutput from Server .... \n" + response + "\n");
        return response;
    }

    /* Put the request in background and send it out */
    @Override
    protected String doInBackground(String... params) {
        String response=null;
        int tryTimes = 0;

        // The request will be sent again for 5 times if it failed.
        while(tryTimes < 5) {
            Date now = new Date();
            response = wrapRequest("Emma", now, now, now, "Polacksbacken", "centrastation202");
            if(sendOutSuccessful) {
                break;
            }
            tryTimes++;
        }
        sendOutSuccessful = false;
        return response;
    }

    /* Deal with the response returned by server */
    @Override
    protected void onPostExecute(String s) {
        super.onPostExecute(s);

        //TODO: set the scrollview with the response
    }
}


