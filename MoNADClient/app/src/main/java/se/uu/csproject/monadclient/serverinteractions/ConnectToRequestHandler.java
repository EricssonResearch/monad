package se.uu.csproject.monadclient.serverinteractions;

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

import se.uu.csproject.monadclient.StoreTrips;
import se.uu.csproject.monadclient.recyclerviews.FullTrip;

public class ConnectToRequestHandler {
    private static final String SERVER = "http://130.238.15.114:2001";
    private static final String ERROR_RESPONSE = "Something went wrong, please try again.";
    private static final String TAG = "oops";

    /* Send the data to the server via POST and receive the response */
    public static String postRequestString(String request, String urlParameters) {
        String response = "";
        HttpURLConnection conn = null;

        try {
            URL url = new URL(SERVER + request);
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
            String line;
            while ((line = br.readLine()) != null) {
                response = response + line;
            }

        } catch (MalformedURLException e) {
            Log.d(TAG, e.toString());
            response = ERROR_RESPONSE;

        } catch (IOException e) {
            Log.d(TAG, e.toString());
            response = ERROR_RESPONSE;

        } catch (RuntimeException e) {
            Log.d(TAG, e.toString());
            response = ERROR_RESPONSE;
        }
        finally {
            if (conn != null) {
                conn.disconnect();
            }
        }

        return response;
    }

    /* Send the data to the server via POST and receive the response */
    public static ArrayList<FullTrip> postRequest(String request, String urlParameters, int searchResultsOrBookings) {
        ArrayList<FullTrip> results = new ArrayList<>();
        HttpURLConnection conn = null;

        try {
            URL url = new URL(SERVER + request);
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

            results = new StoreTrips().storeTheTrips(trips, searchResultsOrBookings);

        } catch (MalformedURLException e) {
            Log.d(TAG, e.toString());

        } catch (IOException e) {
            Log.d(TAG, e.toString());

        } catch (RuntimeException e) {
            Log.d(TAG, e.toString());

        } catch (JSONException e) {
            Log.d(TAG, e.toString());
        }
        finally {
            if (conn != null) {
                conn.disconnect();
            }
        }

        return results;
    }
}
