package se.uu.csproject.monadclient;


import android.os.AsyncTask;
import android.util.Log;

import com.google.common.base.Charsets;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;

public class SendUserBookingsRequestExtra extends AsyncTask<String, Void, ArrayList<FullTrip>> {
    private static String SERVER = "http://130.238.15.114:2001";
    public AsyncResponseMulti delegateMulti = null;

    /* Send the data to the server via POST and receive the response */
    public static ArrayList<FullTrip> postRequest(String request, String urlParameters) {
        ArrayList<FullTrip> bookings = new ArrayList<>();
        HttpURLConnection conn = null;

        try {
            URL url = new URL(request);
            byte[] postData = urlParameters.getBytes(Charsets.UTF_8);
            int postDataLength = postData.length;

            // Setup connection to the server
            conn = (HttpURLConnection)url.openConnection();
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
            if (responseCode != 200) {
                throw new RuntimeException("Something went wrong - HTTP error code: " + responseCode);
            }
            BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"), 8);
            StringBuilder sb = new StringBuilder();
            String inputStr;

            while ((inputStr = br.readLine()) != null){
                sb.append(inputStr);
            }
            JSONObject trips = new JSONObject(sb.toString());

            bookings = new StoreTrips().storeTheTrips(trips, 1);

        } catch (MalformedURLException e) {
            Log.d("oops", e.toString());

        } catch (IOException e) {
            Log.d("oops", e.toString());

        } catch (RuntimeException e) {
            Log.d("oops", e.toString());

        } catch (JSONException e) {
            Log.d("oops", e.toString());
        }
        finally {
            if (conn != null) {
                conn.disconnect();
            }
        }

        return bookings;
    }

    /* Get the data from the interface and wrap them in a request */
    public static ArrayList<FullTrip> wrapRequest(String userId) {
        String request = SERVER + "/getUserBookingsRequest";

        String urlParameters = "userId=" + userId;
        ArrayList<FullTrip> bookings = postRequest(request, urlParameters);

        return bookings;
    }

    /* This is the function that is called by the button listener */
    @Override
    protected ArrayList<FullTrip> doInBackground(String... params) {
        ArrayList<FullTrip> bookings;

        bookings = wrapRequest(params[0]);

        return bookings;
    }

    /* Deal with the response returned by the server */
    @Override
    protected void onPostExecute(ArrayList<FullTrip> bookings) {
        delegateMulti.processFinishMulti(bookings);
    }
}
