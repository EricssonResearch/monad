package se.uu.csproject.monadclient.recyclerviews;

import java.util.ArrayList;
import java.util.Collections;

public class RecommendedTrips {

    private ArrayList<FullTrip> recommendedTrips;

    public RecommendedTrips(){
        this.recommendedTrips = new ArrayList<>();
    }

    public RecommendedTrips(ArrayList<FullTrip> recommendedTrips){
        this.recommendedTrips = recommendedTrips;
    }

    public void insertFullTrip(FullTrip fullTrip){
        recommendedTrips.add(fullTrip);
    }

    public FullTrip getFullTrip(int index){
        return recommendedTrips.get(index);
    }

    public String getId(int index){
        FullTrip trip = recommendedTrips.get(index);
        return trip.getId();
    }

    public void sort(){
        Collections.sort(recommendedTrips, new CustomComparator());
    }
}
