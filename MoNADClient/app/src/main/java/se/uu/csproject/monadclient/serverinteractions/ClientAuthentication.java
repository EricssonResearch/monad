package se.uu.csproject.monadclient.serverinteractions;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;

import se.uu.csproject.monadclient.tools.Security;
import se.uu.csproject.monadclient.storage.BusStop;
import se.uu.csproject.monadclient.storage.FullTrip;
import se.uu.csproject.monadclient.storage.Notify;
import se.uu.csproject.monadclient.storage.PartialTrip;
import se.uu.csproject.monadclient.storage.Storage;

public class ClientAuthentication extends Authentication {
    private static String[] profile = new String[11];

    //only for local use, has nothing to do with database
    private static boolean ifSettingsChanged = false;

    private static boolean ifRecommendNotifyAdded = false;

    /*
     * 0: clientId ("1", "2", ...)
     * 1: username
     * 2: password ("0" or "1")
     * 3: email
     * 4: phone
     * 5: language ("en", ...)
     * 6: storeLocation ("0" or "1")
     * 7: notificationsAlert ("0" or "1")
     * 8 recommendationsAlert ("0" or "1")
     * 9: theme ("0", "1", ...)
     * 10: googleRegistrationToken
     */

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
        } else {
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
        } else {
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
        } else {
            profile[8] = "1";
        }
    }

    public static void setTheme(String theme) {
        profile[9] = theme;
    }

    //theme mappings: 0: light; 1: default; 2: dark
    public static String getTheme() {
        return profile[9];
    }

    public static boolean getIfSettingsChanged(){
        return ifSettingsChanged;
    }

    public static void setIfSettingsChanged(boolean settingsChanged){
        ifSettingsChanged = settingsChanged;
    }

    public static boolean getIfRecommendNotifyAdded(){
        return ifRecommendNotifyAdded;
    }

    public static void setIfRecommendNotifyAdded(boolean recommendNotifyAdded){
        ifRecommendNotifyAdded = recommendNotifyAdded;
    }

    public static void clearGlobalVariables(){
        ifSettingsChanged = false;
        ifRecommendNotifyAdded = false;
    }

    public static void setGoogleRegistrationToken(String googleRegistrationTokenToken) {
        profile[10] = googleRegistrationTokenToken;
    }

    public static String getGoogleRegistrationToken() {
        return profile[10];
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
                          + "\ntheme: " + getTheme()
                          + "\ngoogleRegistrationToken: " + getGoogleRegistrationToken();
        return strProfile;
    }

    public static void initProfile() {
        setClientId("");
        setUsername("");
        setPassword("0");
        setEmail("");
        setPhone("");
        setGoogleRegistrationToken("");
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
        updateProfileData(username, email, phone);
        setPassword(password);
        updateSettings(language, storeLocation, notificationsAlert, recommendationsAlert, theme);
    }

    public static void updateProfileData(String username, String email, String phone) {
        setUsername(username);
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
        setPassword(password);
        updateProfileData(username, email, phone);
        defaultSettings();
    }

    public static String postSignUpRequest(String username, String password, String email, String phone) {

        /* Validate username */
        if (!Security.validateUsername(username)) {
            return Security.invalidUsernameMessage();
        }
        if(!Security.validatePassword(password)){
            return Security.invalidPasswordMessage();
        }
        /* Validate email */
        if (!Security.validateEmail(email)) {
            return Security.invalidEmailMessage();
        }
        /* Validate phone */
        if (!Security.validatePhone(phone)) {
            return Security.invalidPhoneMessage();
        }
        /* Encrypt password */
        password = Security.encryptPassword(password);

        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_sign_up";
        String urlParameters = "username=" + username + "&password=" + password
                + "&email=" + email + "&phone=" + phone
                + "&google_registration_token=" + getGoogleRegistrationToken();

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        return processSignUpResponse(username, email, phone, response);
    }

    public static String processSignUpResponse(String username, String email, String phone, String response) {
        String responseMessage = "";

        /* Username already in use */
        if (response.startsWith("01")) {
            responseMessage = "Username already in use (01)";
        }
        /* Email already in use */
        else if (response.startsWith("02")) {
            responseMessage = "Email already in use (02)";
        }
        /* Phone already in use */
        else if (response.startsWith("03")) {
            responseMessage = "Phone already in use (03)";
        }
        /*
         * Successful signUp request - New client registered to the database
         * Response: "1|clientId"
         */
        else if (response.startsWith("1|")) {
            String clientId = response.substring(2);
            /* updateProfileAfterSignUp(clientId, username, password, email, phone) */
            updateProfileAfterSignUp(clientId, username, "1", email, phone);
            responseMessage = "Success (1) - User Id: " + getClientId();
        } else {
            responseMessage = "ERROR - " + response;
        }
        return responseMessage;
    }

    public static String postSignInRequest(String username, String password) {

        /* Validate username */
        if (!Security.validateUsername(username)) {
            return Security.invalidUsernameMessage();
        }
        /* Encrypt password */
        password = Security.encryptPassword(password);

        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_sign_in";
        String urlParameters = "username=" + username + "&password=" + password
                + "&google_registration_token=" + getGoogleRegistrationToken();

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        return processSignInResponse(username, response);
    }

    public static String processSignInResponse(String username, String response) {
        String responseMessage = "";
        String[] responseData = new String[8];
        /*
         * 0: clientId
         * 1: email
         * 2: phone
         * 3: language
         * 4: storeLocation
         * 5: notificationsAlert
         * 6: recommendationsAlert
         * 7: theme
         */
        String temp = "";
        int index = 0;

        /*
         * Successful signIn request
         * Response: "1|clientId|email|phone|language|
         *              storeLocation|notificationsAlert|recommendationsAlert|theme"
         */
        if (response.startsWith("1|")) {

            /* Process response and parse profile data */
            for (int i = 2; i < response.length(); i++) {
                char c = response.charAt(i);

                if (c != '|') {
                    temp = temp + c;
                } else {
                    responseData[index] = temp;
                    index++;
                    temp = "";
                }
            }
            responseData[index] = temp;

            /* Update profile: clientId, username, password, email, phone,
             *                 language, storeLocation, notificationsAlert,
             *                 recommendationsAlert, theme
             */
            updateProfile(responseData[0], username, "1", responseData[1], responseData[2],
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
        }
        return responseMessage;
    }

    public static String postGoogleSignInRequest(String email) {
        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/google_sign_in";
        String urlParameters = "email=" + email + "&google_registration_token=" + getGoogleRegistrationToken();

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        return processGoogleSignInResponse(email, response);
    }

    public static String processGoogleSignInResponse(String email, String response) {
        String responseMessage = "";
        String[] responseData = new String[9];
        /*
         * 0: clientId
         * 1: username
         * 2: password
         * 3: phone
         * 4: language
         * 5: storeLocation
         * 6: notificationsAlert
         * 7: recommendationsAlert
         * 8: theme
         *
         * email: already exists in the application
         */
        String temp = "";
        int index = 0;

        /*
         * Successful GoogleSignIn request - Client already existed in database
         * Response: "1|clientId|username|password|phone|
         *              language|storeLocation|notificationsAlert|recommendationsAlert|theme"
         */
        if (response.startsWith("1|")) {

            /* Process response and parse profile data */
            for (int i = 2; i < response.length(); i++) {
                char c = response.charAt(i);

                if (c != '|') {
                    temp = temp + c;
                } else {
                    responseData[index] = temp;
                    index++;
                    temp = "";
                }
            }
            responseData[index] = temp;

            /* Update profile: clientId, username, password, email, phone,
             *                 language, storeLocation, notificationsAlert,
             *                 recommendationsAlert, theme
             */
            updateProfile(responseData[0], responseData[1], responseData[2], email, responseData[3],
                    responseData[4], responseData[5], responseData[6],
                    responseData[7], responseData[8]);

            responseMessage = "Success (1) - " + response + profileToString();
        }

        /*
         * Successful GoogleSignIn request - New client registered to the database
         * Response: "2|clientId"
         */
        else if (response.startsWith("2|")) {
            String clientId = response.substring(2);
            /* updateProfileAfterSignUp(clientId, username, password, email, phone) */
            updateProfileAfterSignUp(clientId, "", "0", email, "");
            responseMessage = "Success (1) - User Id: " + getClientId();
        } else {
            responseMessage = "ERROR - " + response;
        }
        return responseMessage;
    }

    public static String postProfileUpdateRequest(String clientId, String username, String email, String phone) {

        /* Validate username */
        if (!Security.validateUsername(username)) {
            return Security.invalidUsernameMessage();
        }
        /* Validate email */
        if (!Security.validateEmail(email)) {
            return Security.invalidEmailMessage();
        }
        /* Validate phone */
        if (!Security.validatePhone(phone)) {
            return Security.invalidPhoneMessage();
        }

        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_profile_update";
        String urlParameters = "client_id=" + clientId + "&username=" + username
                + "&email=" + email + "&phone=" + phone;

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        return processProfileUpdateResponse(username, email, phone, response);
    }

    public static String processProfileUpdateResponse(String username, String email, String phone, String response) {
        String responseMessage = "";

        /* Username already in use */
        if (response.startsWith("01")) {
            responseMessage = "Username already in use (01)";
        }
        /* Email already in use */
        else if (response.startsWith("02")) {
            responseMessage = "Email already in use (02)";
        }
        /* Phone already in use */
        else if (response.startsWith("03")) {
            responseMessage = "Phone already in use (03)";
        }
        /* Successful profileUpdate request */
        else if (response.startsWith("1")) {
            updateProfileData(username, email, phone);
            responseMessage = "Success (1)" + profileToString();
        }
        /* ERROR case */
        else {
            responseMessage = "ERROR - " + response;
        }
        return responseMessage;
    }

    public static String postSettingsUpdateRequest(String clientId, String language,
                                                   String storeLocation, String notificationsAlert,
                                                   String recommendationsAlert, String theme) {

        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_settings_update";
        String urlParameters = "client_id=" + clientId
                + "&language=" + language
                + "&store_location=" + storeLocation
                + "&notifications_alert=" + notificationsAlert
                + "&recommendations_alert=" + recommendationsAlert
                + "&theme=" + theme;

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        return processSettingsUpdateResponse(language, storeLocation, notificationsAlert,
                recommendationsAlert, theme, response);
    }

    public static String processSettingsUpdateResponse(String language, String storeLocation,
                                                       String notificationsAlert, String recommendationsAlert,
                                                       String theme, String response) {
        String responseMessage = "";

        /* Successful settingsUpdateRequest */
        if (response.equals("1")) {
            updateSettings(language, storeLocation, notificationsAlert, recommendationsAlert, theme);
            responseMessage = "Success (1)" + profileToString();
        }
        /* ERROR case */
        else {
            responseMessage = "ERROR - " + response;
        }
        return responseMessage;
    }

    public static String postExistingPasswordUpdateRequest(String clientId, String oldPassword, String newPassword) {
        if(!Security.validatePassword(newPassword)){
            return Security.invalidPasswordMessage();
        }

        /* Encrypt passwords */
        oldPassword = Security.encryptPassword(oldPassword);
        newPassword = Security.encryptPassword(newPassword);

        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_existing_password_update";
        String urlParameters = "client_id=" + clientId
                + "&old_password=" + oldPassword
                + "&new_password=" + newPassword;

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        return processExistingPasswordUpdateResponse(newPassword, response);
    }

    public static String processExistingPasswordUpdateResponse(String newPassword, String response) {
        String responseMessage = "";

        /* Successful existingPasswordUpdateRequest */
        if (response.equals("1")) {
            setPassword(newPassword);
            responseMessage = "Success (1)" + profileToString();
        }
        /* ERROR case */
        else {
            responseMessage = "ERROR - " + response;
        }
        return responseMessage;
    }

    public static String postForgottenPasswordResetRequest(String email, String newPassword) {
        if(!Security.validatePassword(newPassword)){
            return Security.invalidPasswordMessage();
        }

        /* Encrypt password */
        newPassword = Security.encryptPassword(newPassword);

        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/client_forgotten_password_reset";
        String urlParameters = "email=" + email + "&new_password=" + newPassword;

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        // response = response.trim();

        /* Process Authentication Module's response */
        return processForgottenPasswordResetResponse(newPassword, response);
    }

    public static String processForgottenPasswordResetResponse(String newPassword, String response) {
        String responseMessage = "";

        /* Successful existingPasswordUpdateRequest */
        if (response.equals("1")) {
            setPassword(newPassword);
            responseMessage = "Success (1)" + profileToString();
        }
        /* ERROR case */
        else {
            responseMessage = "ERROR - " + response;
        }
        return responseMessage;
    }

    public static String postGetRecommendationsRequest() {
        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/get_recommendations";
        // String urlParameters = "client_id=" + getClientId();
        String urlParameters = "client_id=" + getClientId();

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        return processGetRecommendationsResponse(response);
    }

    public static String processGetRecommendationsResponse(String response) {
        JSONParser parser = new JSONParser();

        try {
            JSONArray recommendations = (JSONArray) parser.parse(response);
            Iterator<JSONObject> recommendationsIterator = recommendations.iterator();

            while (recommendationsIterator.hasNext()) {
                JSONObject recommendation = recommendationsIterator.next();

                JSONObject recommendationObjectID = (JSONObject) recommendation.get("_id");
                String recommendationID = (String) recommendationObjectID.get("$oid");

//                String userID = recommendation.get("userID").toString();

                JSONArray userTripsList = (JSONArray) recommendation.get("userTrip");
                Iterator<JSONObject> userTripsIterator = userTripsList.iterator();

                ArrayList<PartialTrip> partialTrips = new ArrayList<>();

                while (userTripsIterator.hasNext()) {
                    JSONObject trip = userTripsIterator.next();

                    JSONObject tripObjectID = (JSONObject) trip.get("_id");
                    String tripID = (String) tripObjectID.get("$oid");

                    long tempLine = (long) trip.get("line");
                    int line = new BigDecimal(tempLine).intValueExact();

                    long tempBusID = (long) trip.get("busID");
                    int busID = new BigDecimal(tempBusID).intValueExact();

                    String startBusStop = (String) trip.get("startBusStop");
                    JSONObject startTimeObject = (JSONObject) trip.get("startTime");
                    Date startTime = new Date((long) startTimeObject.get("$date"));

                    String endBusStop = (String) trip.get("endBusStop");
                    JSONObject endTimeObject = (JSONObject) trip.get("endTime");
                    Date endTime = new Date((long) endTimeObject.get("$date"));

                    ArrayList<String> trajectory = new ArrayList<>();
                    JSONArray trajectoryArray = (JSONArray) trip.get("trajectory");

                    Iterator<String> trajectoryObjectIterator = trajectoryArray.iterator();
                    while (trajectoryObjectIterator.hasNext()) {
                        String busStopName = trajectoryObjectIterator.next();
                        trajectory.add(busStopName);
                    }

//                    Iterator<JSONArray> trajectoryObjectIterator = trajectoryArray.iterator();
//
//                    /* TODO: Parse specific time for each partial trip */
//                    while (trajectoryObjectIterator.hasNext()) {
//                        String busStopName = (String) trajectoryObjectIterator.next().get(0);
//                        trajectory.add(busStopName);
//                    }

                    PartialTrip partialTrip = new PartialTrip(tripID, line, busID, startBusStop, startTime,
                                                              endBusStop, endTime, trajectory);

                    partialTrips.add(partialTrip);
                }
                FullTrip fullTrip = new FullTrip(partialTrips);
                if (!fullTrip.isHistory()) {
                    Storage.addRecommendation(fullTrip);
                }
//                Storage.addRecommendation(fullTrip);
            }
            Storage.sortRecommendations();
        }
        catch (Exception e) {
            e.printStackTrace();
            return "0";
        }
        return "1";
    }

    public static String postGetNotificationsRequest() {
        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/get_notifications";
        String urlParameters = "client_id=" + getClientId();

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        return processGetNotificationsResponse(response);
    }

    public static String processGetNotificationsResponse(String response) {
        JSONParser parser = new JSONParser();

        try {
            JSONArray notifications = (JSONArray) parser.parse(response);
            Iterator<JSONObject> notificationsIterator = notifications.iterator();

            while (notificationsIterator.hasNext()) {
                JSONObject notification = notificationsIterator.next();

                JSONObject notificationObjectID = (JSONObject) notification.get("_id");
                String notificationID = (String) notificationObjectID.get("$oid");

                String notificationText = (String) notification.get("text");

                JSONObject timeObject = (JSONObject) notification.get("time");
                Date notificationTime = new Date((long) timeObject.get("$date"));

                long temp = (long) notification.get("iconID");
                int notificationIconID = new BigDecimal(temp).intValueExact();

                JSONArray partialTripsList = (JSONArray) notification.get("partialTrips");
                Iterator<JSONObject> partialTripsIterator = partialTripsList.iterator();

                ArrayList<PartialTrip> partialTrips = new ArrayList<>();

                while (partialTripsIterator.hasNext()) {
                    JSONObject trip = partialTripsIterator.next();

                    JSONObject tripObjectID = (JSONObject) trip.get("_id");
                    String tripID = (String) tripObjectID.get("$oid");

                    long tempLine = (long) trip.get("line");
                    int line = new BigDecimal(tempLine).intValueExact();

                    long tempBusID = (long) trip.get("busID");
//                    double tempBusID = (double) trip.get("busID");
                    int busID = new BigDecimal(tempBusID).intValueExact();

                    String startBusStop = (String) trip.get("startBusStop");
                    JSONObject startTimeObject = (JSONObject) trip.get("startTime");
                    Date startTime = new Date((long) startTimeObject.get("$date"));

                    String endBusStop = (String) trip.get("endBusStop");
                    JSONObject endTimeObject = (JSONObject) trip.get("endTime");
                    Date endTime = new Date((long) endTimeObject.get("$date"));

                    ArrayList<String> trajectory = new ArrayList<>();
                    JSONArray trajectoryArray = (JSONArray) trip.get("trajectory");
                    Iterator<String> trajectoryObjectIterator = trajectoryArray.iterator();

                    /* TODO: Parse specific time for each partial trip */
                    while (trajectoryObjectIterator.hasNext()) {
                        String busStopName = trajectoryObjectIterator.next();
                        trajectory.add(busStopName);
                    }

                    PartialTrip partialTrip = new PartialTrip(tripID, line, busID, startBusStop, startTime,
                                                              endBusStop, endTime, trajectory);

                    partialTrips.add(partialTrip);
                }
                FullTrip fullTrip = new FullTrip(partialTrips);

                Notify notify = new Notify(notificationID, notificationText, notificationTime, notificationIconID, fullTrip);
                Storage.addNotification(notify);
            }
            Storage.sortNotifications();
//            Storage.printNotifications();
        }
        catch (Exception e) {
            e.printStackTrace();
            return "0";
        }
        return "1";
    }

    public static String postRemoveNotificationRequest(String notificationID) {
        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/remove_notification";
        String urlParameters = "notification_id=" + notificationID;

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        return processRemoveNotificationResponse(response);
    }

    public static String processRemoveNotificationResponse(String response) {

        if (response.equals("1")) {
            return "1";
        }
        else {
            return "0";
        }
    }

    public static String postGetBusStopsRequest() {
        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/get_bus_stops";
        String urlParameters = "";

        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /* Handle response in case of exception */
        if (response.equals("-1")) {
            return exceptionMessage();
        }

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        return processGetBusStopsResponse(response);
    }

    public static String processGetBusStopsResponse(String response) {
        JSONParser parser = new JSONParser();

        try {
            JSONArray busStopsArray = (JSONArray) parser.parse(response);
            Iterator<JSONObject> busStopsIterator = busStopsArray.iterator();

            ArrayList<BusStop> busStops = new ArrayList<>();

            while (busStopsIterator.hasNext()) {
                JSONObject busStopObject = busStopsIterator.next();

                JSONObject busStopObjectID = (JSONObject) busStopObject.get("_id");
                String busStopID = (String) busStopObjectID.get("$oid");

                String busStopName = (String) busStopObject.get("name");
                double busStopLatitude = (double) busStopObject.get("latitude");
                double busStopLongitude = (double) busStopObject.get("longitude");

                BusStop busStop = new BusStop(busStopID, busStopName, busStopLatitude, busStopLongitude);
                busStops.add(busStop);
            }
            Storage.setBusStops(busStops);
        }
        catch (Exception e) {
            e.printStackTrace();
            return "0";
        }
        return "1";
    }

    public static String exceptionMessage() {
        return "ERROR - An Exception was thrown";
    }
}