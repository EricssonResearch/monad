package se.uu.csproject.monadclient.recyclerviews;

import android.os.Parcel;
import android.os.Parcelable;

import java.util.ArrayList;
import java.util.Collections;

public class Storage{

    private static ArrayList<FullTrip> searchResults = new ArrayList<>();

    public static void setSearchResults(ArrayList<FullTrip> searchResults1){
        searchResults = searchResults1;
    }

    public static ArrayList<FullTrip> getSearchResults(){
        return searchResults;
    }

    public static void clearAll(){
        searchResults.clear();
    }

    public static void sort(){
        Collections.sort(searchResults, new CustomComparator());
    }

    public static boolean isEmpty(){
        if (searchResults != null && !searchResults.isEmpty()){
            return false;
        } else {
            return true;
        }
    }
}
