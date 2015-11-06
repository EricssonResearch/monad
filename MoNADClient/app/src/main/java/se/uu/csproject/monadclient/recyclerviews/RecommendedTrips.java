package se.uu.csproject.monadclient.recyclerviews;

import android.os.Parcel;
import android.os.Parcelable;

import java.util.ArrayList;
import java.util.Collections;

public class RecommendedTrips implements Parcelable {

    private ArrayList<FullTrip> searchResults;

    public RecommendedTrips(){
        this.searchResults = new ArrayList<>();
    }

    public RecommendedTrips(ArrayList<FullTrip> recommendedTrips){
        this.searchResults = recommendedTrips;
    }

    public void insertFullTrip(FullTrip fullTrip){
        searchResults.add(fullTrip);
    }

    public FullTrip getFullTrip(int index){
        return searchResults.get(index);
    }

    public ArrayList<FullTrip> getSearchResults(){
        return searchResults;
    }

    public String getId(int index){
        FullTrip trip = searchResults.get(index);
        return trip.getId();
    }

    public void sort(){
        Collections.sort(searchResults, new CustomComparator());
    }

    public boolean isEmpty(){
        if (searchResults != null && !searchResults.isEmpty()){
            return true;
        } else {
            return false;
        }
    }

    public int describeContents() {
        return this.hashCode();
    }

    public void writeToParcel(Parcel out, int flags) {
        out.writeTypedList(searchResults);
    }

    private RecommendedTrips(Parcel in) {
        in.readTypedList(searchResults, FullTrip.CREATOR);
    }

    public static final Parcelable.Creator<RecommendedTrips> CREATOR = new Parcelable.Creator<RecommendedTrips>() {
        public RecommendedTrips createFromParcel(Parcel in) {
            return new RecommendedTrips(in);
        }

        public RecommendedTrips[] newArray(int size) {
            return new RecommendedTrips[size];
        }
    };
}
