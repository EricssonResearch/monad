package se.uu.csproject.monadclient.recyclerviews;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.GregorianCalendar;

public class Storage{
    private static ArrayList<FullTrip> searchResults = new ArrayList<>();
    private static ArrayList<FullTrip> recommendations = new ArrayList();
    private static ArrayList<Notify> notifications = new ArrayList<>();

    /** Methods for searchResults */
    public static void setSearchResults(ArrayList<FullTrip> searchResults1){
        searchResults = searchResults1;
    }

    public static ArrayList<FullTrip> getSearchResults(){
        return searchResults;
    }

    public static void sortSearchResults() {
        Collections.sort(searchResults, new FullTripsStartTimeComparator());
    }

    public static void clearAll(){
        searchResults.clear();
    }

    public static boolean isEmptySearchResults(){
        if (searchResults != null && !searchResults.isEmpty()){
            return false;
        } else {
            return true;
        }
    }

    /** Methods for recommendations */
    public static ArrayList<FullTrip> getRecommendations() {
        return recommendations;
    }

    public static void setRecommendations(ArrayList<FullTrip> recommendations) {
        Storage.recommendations = recommendations;
    }

    public static void sortRecommendations() {
        Collections.sort(recommendations, new FullTripsStartTimeComparator());
    }

    public static boolean isEmptyRecommendations() {
        if (recommendations != null && !recommendations.isEmpty()) {
            return false;
        }
        else {
            return true;
        }
    }

    public static void addRecommendation(FullTrip recommendation) {
        recommendations.add(recommendation);
    }

    public static void clearRecommendations() {
        recommendations.clear();
    }


    /** Methods for notifications */
    public static ArrayList<Notify> getNotifications() {
        return notifications;
    }

    public static void setNotifications(ArrayList<Notify> notifications) {
        Storage.notifications = notifications;
        sortNotifications();
    }

    public static void sortNotifications() {
        Collections.sort(notifications, new NotificationsTimeComparator());
    }

    public static boolean isEmptyNotifications() {
        if (notifications != null && !notifications.isEmpty()) {
            return false;
        }
        else {
            return true;
        }
    }

    public static void addNotification(Notify notification) {
        notifications.add(notification);
        sortNotifications();
    }

    public static void clearNotifications() {
        notifications.clear();
    }

    public static void removeNotification(int i){
        notifications.remove(i);
    }

    public static void initializeNotificationData(){
        ArrayList<Notify> notifications = new ArrayList<>();
        Calendar calendar = new GregorianCalendar(2015, 10, 26, 10, 40, 0);
        Date time1 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 26, 10, 50, 0);
        Date time2 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 26, 10, 45, 0);
        Date time3 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 26, 11, 0, 0);
        Date time4 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 27, 9, 50, 0);
        Date time5 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 27, 10, 5, 0);
        Date time6 = calendar.getTime();
        notifications.add(new Notify("Bus 805: 5 min delay", time1, 1));
        notifications.add(new Notify("Bus 805: Coming in 5 min", time2, 2));
        notifications.add(new Notify("Bus 805: Departing now", time3, 3));
        notifications.add(new Notify("Bus 801: 5 min delay", time4, 1));
        notifications.add(new Notify("Bus 801: Coming in 5 min", time5, 2));
        notifications.add(new Notify("Bus 801: Departing now", time6, 3));
        setNotifications(notifications);
    }

}

