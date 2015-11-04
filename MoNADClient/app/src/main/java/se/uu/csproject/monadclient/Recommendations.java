package se.uu.csproject.monadclient;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.ArrayList;
import java.util.Iterator;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import java.util.Date;
import java.util.List;

import se.uu.csproject.monadclient.recyclerviews.Trip;

/**
 *
 */
public class Recommendations extends Authentication {

    public static List<Trip> getRecommendations() {
        String request = AUTHENTICATION_HOST + AUTHENTICATION_PORT + "/get_recommendations";
        // String urlParameters = "client_id=" + getClientId();
        String urlParameters = "client_id=" + ClientAuthentication.getClientId();
        /* Send the request to the Authentication Module */
        String response = postRequest(request, urlParameters);

        /*
         * By default, Erlang adds the newline '\n' character at the beginning of response.
         * For this reason substring() function is used
         */
        response = response.substring(1);
        JSONParser parser = new JSONParser();
        List<Trip> recommendations = new ArrayList<>();

        try {
            JSONArray recommendation = (JSONArray) parser.parse(response);
            Iterator<JSONObject> iterator = recommendation.iterator();

            while (iterator.hasNext()){
                JSONObject info = iterator.next();
                JSONObject id = (JSONObject) info.get("_id");
                String oid = id.get("$oid").toString();
                String userId = info.get("userId").toString();
                JSONArray recList = (JSONArray) info.get("recommendations");
                Iterator<JSONObject> recListIterator = recList.iterator();
                int index = 0;

                while (recListIterator.hasNext()) {
                    index++;
                    JSONObject trip = recListIterator.next();
                    String startPlace = trip.get("startPlace").toString();
                    String endPlace = trip.get("endPlace").toString();
                    JSONObject startTime = (JSONObject) trip.get("startTime");
                    Date sTime = new Date((long)startTime.get("$date"));
                    JSONObject endTime = (JSONObject) trip.get("endTime");
                    Date eTime = new Date((long)endTime.get("$date"));
                    long vehicleNo = (long) trip.get("vehicleNo");
                    JSONObject routeId = (JSONObject) trip.get("routeId");
                    String rId = (String) routeId.get("$oid");
                    int duration = (int) (eTime.getTime() - sTime.getTime());

//                    printInfo(startPlace, endPlace, sTime, eTime, vehicleNo, rId, duration);

                    Trip tTrip = new Trip(index, startPlace, sTime, endPlace, eTime, duration, -1);
                    recommendations.add(tTrip);
                }
            }
        }

        catch (ParseException e) {
            System.out.println("failed: parse exception" + e);
        }
        return recommendations;
    }

    public static void printInfo(String start, String end, Date sTime, Date eTime, long vNo, String rId, long duration){

        System.out.printf("%nStart Place: %10s, End Place: %10s%nStart Time: %15tD, End Time: %15tD%n"+
                "Vehicle No.: %15d, Route: %15s, Duration: %10tD%n%n", start, end, sTime, eTime, vNo, rId, duration);
    }

//     public static void main(String[] args) {
//         getRecommendations("1003634");
// }
}