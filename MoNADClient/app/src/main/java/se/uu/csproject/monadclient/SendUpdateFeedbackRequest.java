package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

import com.google.common.base.Charsets;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


public class SendUpdateFeedbackRequest extends AsyncTask<String, Void, String> {
    private static String SERVER = "http://130.238.15.114:2001";
    private static String ERROR_RESPONSE = "Something went wrong, please try again.";
    public AsyncResponseString delegate = null;

    /* Send the data to the server via POST and receive the response */
    public static String postRequest(String request, String urlParameters) {
        String response = "";
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
            String line;
            while ((line = br.readLine()) != null) {
                response = response + line;
            }

        } catch (MalformedURLException e) {
            Log.d("oops", e.toString());
            response = ERROR_RESPONSE;

        } catch (IOException e) {
            Log.d("oops", e.toString());
            response = ERROR_RESPONSE;

        } catch (RuntimeException e) {
            Log.d("oops", e.toString());
            response = ERROR_RESPONSE;
        }
        finally {
            if (conn != null) {
                conn.disconnect();
            }
        }

        return response;
    }

    /* Get the data from the interface and wrap them in a request */
    public static String wrapRequest(String changedFeedback) {
        String request = SERVER + "/updateFeedbackRequest";

        String urlParameters = "changedFeedback=" + changedFeedback;
        String response = postRequest(request, urlParameters);

        return response;
    }

    /* This is the function that is called by the button listener */
    @Override
    protected String doInBackground(String... params) {
        String response;

        response = wrapRequest(params[0]);

        return response;
    }

    /* Deal with the response returned by the server */
    @Override
    protected void onPostExecute(String response) {
        delegate.processFinish(response);
    }
}
