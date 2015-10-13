package se.uu.csproject.monadclient;

import java.net.URL;
import java.net.HttpURLConnection;
import java.io.DataOutputStream;
import java.io.BufferedReader;
import java.nio.charset.StandardCharsets;
import java.io.InputStreamReader;
import java.io.IOException;

/**
 *
 */

public class ClientAuthentication {
    private static final String AUTHENTICATION_HOST = "";
    private static final String AUTHENTICATION_PORT = "";
    private static String[] profile = new String[9];
    /* 0: clientId */
    /* 1: username */
    /* 2: password */
    /* 3: email */
    /* 4: phone */
    /* 5: language */
    /* 6: storeLocation */
    /* 7: notificationsAlert */
    /* 8 recommendationsAlert */

    public static void setClientId(String clientId) {
        profile[0] = clientId;
    }
    public static String getClientId() {
        return profile[0];
    }

    public static void setUsername(String username) {
        profile[1] = username;
    }
    public static String getUsername() {
        return profile[1];
    }

    public static void setPassword(String password) {
        profile[2] = password;
    }
    public static String getPassword() {
        return profile[2];
    }

    public static void setEmail(String email) {
        profile[3] = email;
    }
    public static String getEmail() {
        return profile[3];
    }

    public static void setPhone(String phone) {
        profile[4] = phone;
    }
    public static String getPhone() {
        return profile[4];
    }

    public static void setLanguage(String language) {
        profile[5] = language;
    }
    public static String getLanguage() {
        return profile[5];
    }

    public static void setStoreLocation(String storeLocation) {
        profile[6] = storeLocation;
    }
    public static String getStoreLocation() {
        return profile[6];
    }
    public static void updateStoreLocation() {

        if (profile[6].equalsIgnoreCase("1")) {
            profile[6] = "0";
        }
        else {
            profile[6] = "1";
        }
    }

    public static void setNotificationsAlert(String notificationsAlert) {
        profile[7] = notificationsAlert;
    }
    public static String getNotificationsAlert() {
        return profile[7];
    }
    public static void updateNotificationsAlert() {

        if (profile[7].equalsIgnoreCase("1")) {
            profile[7] = "0";
        }
        else {
            profile[7] = "1";
        }
    }

    public static void setRecommendationsAlert(String recommendationsAlert) {
        profile[8] = recommendationsAlert;
    }
    public static String getRecommendationsAlert() {
        return profile[8];
    }
    public static void updateRecommendationsAlert() {

        if (profile[8].equalsIgnoreCase("1")) {
            profile[8] = "0";
        }
        else {
            profile[8] = "1";
        }
    }

    public static void defaultSettings() {
        setLanguage("en");
        setStoreLocation("1");
        setNotificationsAlert("1");
        setRecommendationsAlert("1");
    }

    public static void initProfile() {
        setClientId("");
        setUsername("");
        setPassword("");
        setEmail("");
        setPhone("");
        defaultSettings();
    }

    public static void updateProfile(String username, String password, String email, String phone) {
        setUsername(username);
        setPassword(password);
        setEmail(email);
        setPhone(phone);
    }

    public static void setProfileBeforeSignUp(String username, String password, String email, String phone) {
        setUsername(username);
        setPassword(password);
        setEmail(email);
        setPhone(phone);
        // defaultSettings();
    }

    public static void setProfileAfterSignUp(String clientId) {
        setClientId(clientId);
    }

    public static void setProfileBeforeGoogleSignUp(String email) {
        setEmail(email);
        // defaultSettings();
    }

    public static void setProfileAfterGoogleSignUp(String clientId) {
        setClientId(clientId);
    }

    public static void setProfileBeforeSignIn(String username, String password) {
        setUsername(username);
        setPassword(password);
    }

    public static void setProfileAfterSignIn(String clientId, String email, String phone,
                                             String language, String storeLocation,
                                             String notificationsAlert, String recommendationsAlert) {
        setClientId(clientId);
        setEmail(email);
        setPhone(phone);
        setLanguage(language);
        setStoreLocation(storeLocation);
        setNotificationsAlert(notificationsAlert);
        setRecommendationsAlert(recommendationsAlert);
    }

    public static String postRequest(String request, String urlParameters) {
        String response = "";
        URL url = null;
        HttpURLConnection connection = null;
        DataOutputStream dos = null;
        BufferedReader br = null;

        try {
            url = new URL(request);
            byte[] postData = urlParameters.getBytes(StandardCharsets.UTF_8);
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

    public static void postSignUpRequest(String username, String password, String email, String phone) {
        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_sign_up";
        String urlParameters = "username=" + username + "&password=" + password
                             + "&email=" + email + "&phone=" + phone;

        /* Update profile: username, password, email, phone */
        setProfileBeforeSignUp(username, password, email, phone);

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* By default, Erlang adds the newline '\n' character at the beginning of response */
        /* For this reason substring() function is used */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        processSignUpResponse(response);
    }

    public static void processSignUpResponse(String response) {
        String responseMessage = "";

        /* Username already in use */
        if (response.startsWith("01")) {
            responseMessage = "Username already in use (2)";
        }
        /* Email already in use */
        else if (response.startsWith("02")) {
            responseMessage = "Email already in use (3)";
        }
        /* Phone already in use */
        else if (response.startsWith("03")) {
            responseMessage = "Phone already in use (4)";
        }
        /* Successful signUp request */
        /* Response: "1|clientId" */
        else if (response.startsWith("1|")) {
            /* Update profile: clientId */
            setProfileAfterSignUp(response.substring(2));
            responseMessage = "Success (1) - User Id: " + getClientId();
        }
        else {
            System.out.println("ERROR - " + response);
        }
        System.out.println("Response: " + responseMessage);
    }

    public static void postSignInRequest(String username, String password) {
        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_sign_in";
        String urlParameters = "username=" + username + "&password=" + password;

        /* Update profile: username, password */
        setProfileBeforeSignIn(username, password);

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* By default, Erlang adds the newline '\n' character at the beginning of response */
        /* For this reason substring() function is used */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        processSignInResponse(response);
    }

    public static void processSignInResponse(String response) {
        String responseMessage = "";
        String[] responseData = new String[7];
        /* 0: id */
        /* 1: email */
        /* 2: phone */
        /* 3: language */
        /* 4: storeLocation */
        /* 5: notificationsAlert */
        /* 6 recommendationsAlert */
        String temp = "";
        int index = 0;

        /* Successful signIn request */
        /* Response: "1|clientId|email|phone|language|storeLocation|notificationsAlert|recommendationsAlert" */
        if (response.startsWith("1|")) {

            /* Process response and parse profile data */
            for (int i = 2; i < response.length(); i++) {
                char c = response.charAt(i);

                if (c != '|') {
                    temp = temp + c;
                }
                else {
                    responseData[index] = temp;
                    index++;
                    temp = "";
                }
            }
            responseData[index] = temp;

            /* Update profile: clientId, email, phone, language,
                               storeLocation, notificationsAlert, recommendationsAlert */
            setProfileAfterSignIn(responseData[0], responseData[1], responseData[2], responseData[3],
                                  responseData[4], responseData[5], responseData[6]);

            responseMessage = "Success (1) - " + response
                    + "\nclientId: " + getClientId()
                    + "\nemail: " + getEmail()
                    + "\nphone: " + getPhone()
                    + "\nlanguage: " + getLanguage()
                    + "\nstoreLocation: " + getStoreLocation()
                    + "\nnotificationsAlert: " + getNotificationsAlert()
                    + "\nrecommendationsAlert: " + getRecommendationsAlert();
        }
        /* Wrong crendentials */
        else if (response.startsWith("0")) {
            responseMessage = "Wrong Crendentials (0)";
        }
        /* ERROR case */
        else {
            System.out.println("ERROR - " + response);
        }
        System.out.println("\nResponse: " + responseMessage);
    }
}