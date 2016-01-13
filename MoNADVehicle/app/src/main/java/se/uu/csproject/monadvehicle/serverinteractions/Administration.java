package se.uu.csproject.monadvehicle.serverinteractions;

import com.google.common.base.Charsets;
import java.net.URL;
import java.net.HttpURLConnection;
import java.io.DataOutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public abstract class Administration {
    public static final String ROUTES_ADMINISTRATOR_HOST = "http://130.238.15.114:";
    public static final String ROUTES_ADMINISTRATOR_PORT = "9997";

    public static final String ROUTES_GENERATOR_HOST = "http://130.238.15.114:";
    public static final String ROUTES_GENERATOR_PORT = "9998";

    public static String postRequest(String request, String urlParameters) {
        String response = "";
        HttpURLConnection connection = null;

        try {
            URL url = new URL(request);
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

            DataOutputStream dos = new DataOutputStream(connection.getOutputStream());
            dos.write(postData);

            /* Case of exception */
            if (connection.getResponseCode() != 200) {
                return "-1";
            }
            BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line;

            while ((line = br.readLine()) != null) {
                response = response + "\n" + line;
            }
            br.close();
            dos.close();
            connection.disconnect();
        }
        catch (Exception e) {
            e.printStackTrace();
            return "-1";
        }
        finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
        return response;
    }
}