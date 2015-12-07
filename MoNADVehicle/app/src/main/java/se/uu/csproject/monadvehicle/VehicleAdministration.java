package se.uu.csproject.monadvehicle;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.mapsforge.core.model.LatLong;

import java.math.BigDecimal;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
import java.util.TimeZone;


/**
 *
 */
public class VehicleAdministration extends Administration {
    public static String[] profile = new String[5];
    /*
     * 0: vehicleID
     * 1: driverID
     * 2: password
     * 3: busLine
     * 4: googleRegistrationToken
     */

    public static String getVehicleID() {
        return profile[0];
    }
    public static void setVehicleID(String vehicleID) {
        profile[0] = vehicleID;
    }

    public static String getDriverID() {
        return profile[1];
    }
    public static void setDriverID(String driverID) {
        profile[1] = driverID;
    }

    public static String getPassword() {
        return profile[2];
    }
    public static void setPassword(String password) {
        profile[2] = password;
    }

    public static String getBusLine() {
        return profile[3];
    }
    public static void setBusLine(String busLine) {
        profile[3] = busLine;
    }

    public static String getGoogleRegistrationToken() {
        return profile[4];
    }
    public static void setGoogleRegistrationToken(String googleRegistrationToken) {
        profile[4] = googleRegistrationToken;
    }

    public static void updateProfileAfterSignIn(String vehicleID, String driverID, String password, String busLine) {
        setVehicleID(vehicleID);
        setDriverID(driverID);
        setPassword(password);
        setBusLine(busLine);
        setGoogleRegistrationToken("");
    }

    public static String profileToString() {
        return "\nVehicleID: " + getVehicleID()
                + "\nDriverID: " + getDriverID()
                + "\nPassword: " + getPassword()
                + "\nBusLine: " + getBusLine()
                + "\nGoogleRegistrationToken: " + getGoogleRegistrationToken();
    }

    public static String postSignInRequest(String driverID, String password, String busLine) {

        /* Encrypt password */
//        password = Security.encryptPassword(password);

        String request = ROUTES_ADMINISTRATOR_HOST + ROUTES_ADMINISTRATOR_PORT + "/vehicle_sign_in";
        String urlParameters = "driver_id=" + driverID + "&password=" + password + "&bus_line=" + busLine;

        /* Send the request to the Routes Administrator */
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

        /* Process Routes Administrator's response */
        return processSignInResponse(driverID, password, busLine, response);
    }

    public static String processSignInResponse(String driverID, String password, String busLine, String response) {
        /*
         * Successful signIn request
         * Response: "1|vehicleID"
         */
        if (response.startsWith("1|")) {
            String vehicleID = response.substring(2);
            updateProfileAfterSignIn(vehicleID, driverID, password, busLine);
            return "Success (1) - VehicleID: " + getVehicleID();
        }
        else if (response.equals("0")) {
            return "Wrong Credentials (0)";
        }
        else {
            return "ERROR - " + response;
        }
    }

    public static String postGetNextTripRequest() {
        String request = ROUTES_ADMINISTRATOR_HOST + ROUTES_ADMINISTRATOR_PORT + "/vehicle_get_next_trip";
        String urlParameters = "vehicle_id=" + getVehicleID();

        /* Send the request to the Routes Administrator */
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

        /* Process Routes Administrator's response */
        return processGetNextTripResponse(response);
    }

    public static String processGetNextTripResponse(String response) {
        JSONParser parser = new JSONParser();

        try {
            JSONObject busTripObject = (JSONObject) parser.parse(response);

            JSONObject busTripObjectID = (JSONObject) busTripObject.get("_id");
            String busTripID = (String) busTripObjectID.get("$oid");

            long tempCapacity = (long) busTripObject.get("capacity");
            int capacity = new BigDecimal(tempCapacity).intValueExact();

//            long tempLine = (long) busTripObject.get("line");
//            int line = new BigDecimal(tempLine).intValueExact();

            JSONArray trajectoryArray = (JSONArray) busTripObject.get("trajectory");
            Iterator<JSONObject> trajectoryArrayIterator = trajectoryArray.iterator();

            ArrayList<BusStop> trajectory = new ArrayList<>();

            while (trajectoryArrayIterator.hasNext()) {

                JSONObject trajectoryPoint = trajectoryArrayIterator.next();
                JSONObject busStopObject = (JSONObject) trajectoryPoint.get("busStop");

                JSONObject busStopObjectID = (JSONObject) busStopObject.get("_id");
                String busStopID = (String) busStopObjectID.get("$oid");

                String busStopName = (String) busStopObject.get("name");

                double busStopLatitude = (double) busStopObject.get("latitude");
                double busStopLongitude = (double) busStopObject.get("longitude");

                JSONObject arrivalTimeObject = (JSONObject) trajectoryPoint.get("time");
                Date busStopArrivalTime = new Date((long) arrivalTimeObject.get("$date"));

                BusStop busStop = new BusStop(busStopID, busStopName, busStopLatitude, busStopLongitude, busStopArrivalTime);
                trajectory.add(busStop);
            }

            BusTrip busTrip = new BusTrip(busTripID, capacity, trajectory);
            Storage.setBusTrip(busTrip);
            busTrip.printBusStops();
//            postGetTrajectoryRequest();
        }
        catch (Exception e) {
            e.printStackTrace();
            return "0";
        }
        return "1";
    }

    public static String postGetTrajectoryRequest() {
        String request = ROUTES_GENERATOR_HOST + ROUTES_GENERATOR_PORT + "/get_route_from_coordinates";
        String urlParameters = getBusStopCoordinates();

        /* Send the request to the Route Generator */
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

        /* Process Route Generator's response */
        return processGetTrajectoryResponse(response);
    }

    public static String getBusStopCoordinates() {
        String data = "";
        BusTrip busTrip = Storage.getBusTrip();

        if (busTrip != null && busTrip.getBusStops() != null) {

            String list = "[";

            for (int i = 0; i < busTrip.getBusStops().size(); i++) {
                list = list + busTrip.getBusStops().get(i).coordinatesToString();

                if (i < busTrip.getBusStops().size() - 1) {
                    list = list + ", ";
                }
            }
            list = list + "]";
            data = "list=" + list;
        }
        return data;
    }

    public static String processGetTrajectoryResponse(String response) {
        JSONParser parser = new JSONParser();

        try {
            JSONObject trajectoryObject = (JSONObject) parser.parse(response);
            String route = (String) trajectoryObject.get("route");
            ArrayList<String> trajectoryPoints = new ArrayList<>();
            String coordinate = "";

            for (int i = 0; i < route.length(); i++) {

                if ((route.charAt(i) >= '0' && route.charAt(i) <= '9') || route.charAt(i) == '.') {
                    coordinate = coordinate + route.charAt(i);
                }
                else if ((route.charAt(i) == ',' || route.charAt(i) == ')') && !coordinate.equals("")) {
                    trajectoryPoints.add(coordinate);
                    coordinate = "";
                }
                else {}
            }
            BusTrip busTrip = Storage.getBusTrip();
            ArrayList<LatLong> trajectory = new ArrayList<>();

            for (int i = 0; i < trajectoryPoints.size() - 1; i = i + 2) {
                trajectory.add(new LatLong(Double.parseDouble(trajectoryPoints.get(i + 1)),
                                           Double.parseDouble(trajectoryPoints.get(i))));
            }
            busTrip.setTrajectory(trajectory);
            busTrip.printTrajectory();
        }
        catch (Exception e) {
            e.printStackTrace();
            return "0";
        }
        return "1";
    }

    public static String postGetPassengersRequest(String busTripID, String currentBusStop, String nextBusStop) {
        String request = ROUTES_ADMINISTRATOR_HOST + ROUTES_ADMINISTRATOR_PORT + "/get_passengers";
        String urlParameters = "bus_trip_id=" + busTripID
                             + "&current_bus_stop=" + currentBusStop
                             + "&next_bus_stop=" + nextBusStop;

        /* Send the request to the RoutesAdministrator */
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

        /* Process response */
        return processGetPassengersResponse(response);
    }

    public static String processGetPassengersResponse(String response) {
        JSONParser parser = new JSONParser();

        try {
            JSONObject getPassengersObject = (JSONObject) parser.parse(response);

            long tempBoarding = (long) getPassengersObject.get("boarding");
            int boarding = new BigDecimal(tempBoarding).intValueExact();

            long tempDeparting = (long) getPassengersObject.get("departing");
            int departing = new BigDecimal(tempDeparting).intValueExact();

            Storage.getBusTrip().setBoardingPassengers(boarding);
            Storage.getBusTrip().setDepartingPassengers(departing);
        }
        catch (Exception e) {
            e.printStackTrace();
            return "0";
        }
        return "1";
    }

    public static String postGetTrafficInformationRequest() {
        String request = ROUTES_ADMINISTRATOR_HOST + ROUTES_ADMINISTRATOR_PORT + "/get_traffic_information";
        String urlParameters = "";

        /* Send the request to the RoutesAdministrator */
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

        /* Process response */
        return processGetTrafficInformationResponse(response);
    }

    public static String processGetTrafficInformationResponse(String response) {
//        System.out.println("Response: " + response);
        JSONParser parser = new JSONParser();

        try {
            JSONArray trafficInformationArray = (JSONArray) parser.parse(response);
            Iterator<JSONObject> trafficInformationArrayIterator = trafficInformationArray.iterator();
            ArrayList<TrafficInformation> trafficIncidents = new ArrayList<>();

            while (trafficInformationArrayIterator.hasNext()) {
                JSONObject trafficInformationObject = (JSONObject) trafficInformationArrayIterator.next();

                String temp = (String) trafficInformationObject.get("StartPointLatitude");
                double startPointLatitude = Double.parseDouble(temp);

                temp = (String) trafficInformationObject.get("StartPointLongitude");
                double startPointLongitude = Double.parseDouble(temp);

                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
                sdf.setTimeZone(TimeZone.getTimeZone("UTC"));

                temp = ((String) trafficInformationObject.get("LastModifiedUTC")).substring(0, 19);
                Date lastModifiedUTC = sdf.parse(temp);

                temp = ((String) trafficInformationObject.get("StartTimeUTC")).substring(0, 19);
                Date startTimeUTC = sdf.parse(temp);

                temp = ((String) trafficInformationObject.get("EndTimeUTC")).substring(0, 19);
                Date endTimeUTC = sdf.parse(temp);

                String incidentType = (String) trafficInformationObject.get("IncidentType");
                String incidentSeverity = (String) trafficInformationObject.get("IncidentSeverity");

                temp = (String) trafficInformationObject.get("RoadClosed");
                boolean roadClosed = Boolean.parseBoolean(temp);

                String description = (String) trafficInformationObject.get("Description");

                temp = (String) trafficInformationObject.get("StopPointLatitude");
                double stopPointLatitude = Double.parseDouble(temp);

                temp = (String) trafficInformationObject.get("StopPointLongitude");
                double stopPointLongitude = Double.parseDouble(temp);

                TrafficInformation trafficInformation = new TrafficInformation(
                        startPointLatitude, startPointLongitude, lastModifiedUTC, startTimeUTC,
                        endTimeUTC, incidentType, incidentSeverity, roadClosed, description,
                        stopPointLatitude, stopPointLongitude);

                trafficIncidents.add(trafficInformation);
            }
            Storage.setTrafficIncidents(trafficIncidents);
        }
        catch (Exception e) {
            e.printStackTrace();
            return "0";
        }
        return "1";
    }

    public static String postSetGoogleRegistrationTokenRequest() {
        String request = ROUTES_ADMINISTRATOR_HOST + ROUTES_ADMINISTRATOR_PORT + "/set_google_registration_token";
        String urlParameters = "vehicle_id=" + getVehicleID()
                             + "&google_registration_token=" + getGoogleRegistrationToken();

        /* Send the request to the RoutesAdministrator */
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
        return response;
    }

    public static String exceptionMessage() {
        return "ERROR - An Exception was thrown";
    }

}
