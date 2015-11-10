package se.uu.csproject.monadclient.recyclerviews;

import java.util.ArrayList;
import java.util.Collections;

public class Storage{
    private static ArrayList<FullTrip> searchResults = new ArrayList<>();
    private static ArrayList<FullTrip> recommendations = new ArrayList();

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
}
