package se.uu.csproject.monadclient;

//import com.google.common.base.Charsets;

/**
 *
 */
public class ClientAuthentication extends Authentication {
    private static String[] profile = new String[10];
    /* 0: clientId */
    /* 1: username */
    /* 2: password */
    /* 3: email */
    /* 4: phone */
    /* 5: language */
    /* 6: storeLocation */
    /* 7: notificationsAlert */
    /* 8 recommendationsAlert */
    /* 9: theme */

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

    public static void setTheme(String theme) {
        profile[9] = theme;
    }
    public static String getTheme() {
        return profile[9];
    }

    public static String profileToString() {
        String strProfile = "\nclientId: " + getClientId()
                + "\nusername: " + getUsername()
                + "\npassword: " + getPassword()
                + "\nemail: " + getEmail()
                + "\nphone: " + getPhone()
                + "\nlanguage: " + getLanguage()
                + "\nstoreLocation: " + getStoreLocation()
                + "\nnotificationsAlert: " + getNotificationsAlert()
                + "\nrecommendationsAlert: " + getRecommendationsAlert()
                + "\ntheme: " + getTheme();
        return strProfile;
    }

    public static void initProfile() {
        setClientId("");
        setUsername("");
        setPassword("");
        setEmail("");
        setPhone("");
        defaultSettings();
    }

    public static void defaultSettings() {
        setLanguage("en");
        setStoreLocation("1");
        setNotificationsAlert("1");
        setRecommendationsAlert("1");
        setTheme("1");
    }

    public static void updateProfile(String clientId, String username, String password, String email, String phone,
                                     String language, String storeLocation, String notificationsAlert,
                                     String recommendationsAlert, String theme) {
        setClientId(clientId);
        updateProfileData(username, password, email, phone);
        updateSettings(language, storeLocation, notificationsAlert, recommendationsAlert, theme);
    }

    public static void updateProfileData(String username, String password, String email, String phone) {
        setUsername(username);
        setPassword(password);
        setEmail(email);
        setPhone(phone);
    }

    public static void updateSettings(String language, String storeLocation, String notificationsAlert,
                                      String recommendationsAlert, String theme) {
        setLanguage(language);
        setStoreLocation(storeLocation);
        setNotificationsAlert(notificationsAlert);
        setRecommendationsAlert(recommendationsAlert);
        setTheme(theme);
    }

    public static void updateProfileAfterSignUp(String clientId, String username, String password,
                                                String email, String phone) {
        setClientId(clientId);
        setUsername(username);
        setPassword(password);
        setEmail(email);
        setPhone(phone);
        defaultSettings();
    }

    // public static void setProfileBeforeGoogleSignUp(String email) {
    //     setEmail(email);
    //     // defaultSettings();
    // }
    //
    // public static void setProfileAfterGoogleSignUp(String clientId) {
    //     setClientId(clientId);
    // }
    //

    public static String postSignUpRequest(String username, String password, String email, String phone) {
        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_sign_up";
        String urlParameters = "username=" + username + "&password=" + password
                             + "&email=" + email + "&phone=" + phone;

        /* Update profile: username, password, email, phone */
        // setProfileBeforeSignUp(username, password, email, phone);

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* By default, Erlang adds the newline '\n' character at the beginning of response */
        /* For this reason substring() function is used */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        return processSignUpResponse(username, password, email, phone, response);
    }

    public static String processSignUpResponse(String username, String password, String email,
                                             String phone, String response) {
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
            /* Update profile: clientId, username, password, email, phone */
            String clientId = response.substring(2);
            updateProfileAfterSignUp(clientId, username, password, email, phone);
            responseMessage = "Success (1) - User Id: " + getClientId();
        }
        else {
            responseMessage = "ERROR - " + response;
//            System.out.println("ERROR - " + response);
        }
//        System.out.println("Response: " + responseMessage);
        return responseMessage;
    }

    public static String postSignInRequest(String username, String password) {
        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_sign_in";
        String urlParameters = "username=" + username + "&password=" + password;

        /* Update profile: username, password */
        // setProfileBeforeSignIn(username, password);

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* By default, Erlang adds the newline '\n' character at the beginning of response */
        /* For this reason substring() function is used */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        return processSignInResponse(username, password, response);
    }

    public static String processSignInResponse(String username, String password, String response) {
        String responseMessage = "";
        String[] responseData = new String[8];
        /* 0: id */
        /* 1: email */
        /* 2: phone */
        /* 3: language */
        /* 4: storeLocation */
        /* 5: notificationsAlert */
        /* 6 recommendationsAlert */
        /* 7: theme */
        String temp = "";
        int index = 0;

        /* Successful signIn request */
        /* Response: "1|clientId|email|phone|language|storeLocation|notificationsAlert|recommendationsAlert|theme" */
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

            /* Update profile: clientId, username, password, email, phone,
                               language, storeLocation, notificationsAlert,
                               recommendationsAlert, theme */
            updateProfile(responseData[0], username, password, responseData[1], responseData[2],
                    responseData[3], responseData[4], responseData[5],
                    responseData[6], responseData[7]);

            responseMessage = "Success (1) - " + response + profileToString();
        }
        /* Wrong credentials */
        else if (response.startsWith("0")) {
            responseMessage = "Wrong Credentials (0)";
        }
        /* ERROR case */
        else {
            responseMessage = "ERROR - " + response;
//            System.out.println("ERROR - " + response);
        }
//        System.out.println("\nResponse: " + responseMessage);
        return responseMessage;
    }

    public static void postProfileUpdateRequest(String clientId, String username, String password,
                                                String email, String phone) {

        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_profile_update";
        String urlParameters = "client_id=" + clientId + "&username=" + username
                + "&password=" + password + "&email=" + email + "&phone=" + phone;

        /* Update profile: username, password, email, phone */
        // setProfileBeforeSignUp(username, password, email, phone);

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* By default, Erlang adds the newline '\n' character at the beginning of response */
        /* For this reason substring() function is used */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        processProfileUpdateResponse(username, password, email, phone, response);
    }

    //// TODO Lefteris: implement processProfileUpdateResponse and return meaningful response message as string
    public static void processProfileUpdateResponse(String username, String password, String email,
                                                    String phone, String response) {

    }
}

//responseMessage = "Welcome " + getUsername() + " !";
//responseMessage = "Welcome back " + getUsername() + " !";
//responseMessage = "The password or username is not correct.";