package se.uu.csproject.monadclient;

import com.google.common.base.Charsets;
import java.net.URL;
import java.net.HttpURLConnection;
import java.io.DataOutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

/**
 *
 */
public abstract class Authentication {
    /* "http://localhost:" "http://130.238.15.114:" */
    public static final String AUTHENTICATION_HOST = "http://130.238.15.114:";
    public static final String AUTHENTICATION_PORT = "9999";

    public static String postRequest(String request, String urlParameters) {
        String response = "";
        URL url = null;
        HttpURLConnection connection = null;
        DataOutputStream dos = null;
        BufferedReader br = null;

        try {
            url = new URL(request);
            byte[] postData = urlParameters.getBytes(Charsets.UTF_8);
            int postDataLength = postData.length;

            connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            connection.setInstanceFollowRedirects(false);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            connection.setRequestProperty("charset", "utf-8");
            connection.setRequestProperty("Content-Length", Integer.toString(postDataLength));
            connection.setUseCaches(false);

            dos = new DataOutputStream(connection.getOutputStream());
            dos.write(postData);

            if (connection.getResponseCode() != 200) {
                throw new RuntimeException("Failed : HTTP error code : " + connection.getResponseCode());
            }
            br = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line = "";

            while ((line = br.readLine()) != null) {
                response = response + "\n" + line;
            }
            br.close();
            dos.close();
            connection.disconnect();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
        finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
        return response;
    }
}