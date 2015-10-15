package se.uu.csproject.monadclient.recyclerviews;

import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.List;

import se.uu.csproject.monadclient.R;

public class SearchRecyclerViewAdapter extends RecyclerView.Adapter<SearchRecyclerViewAdapter.SearchViewHolder>{

    public static class SearchViewHolder extends RecyclerView.ViewHolder {

        TextView timeInfo;
        TextView routeInfo;
        ImageView hurryAlertIcon;

        SearchViewHolder(View itemView) {
            super(itemView);
            timeInfo = (TextView) itemView.findViewById(R.id.label_timeinfo);
            routeInfo = (TextView) itemView.findViewById(R.id.label_routeinfo);
            hurryAlertIcon = (ImageView) itemView.findViewById(R.id.icon_hurry);
        }
    }

    List<Trip> searchResults;

    public SearchRecyclerViewAdapter(List<Trip> searchResults){
        this.searchResults = searchResults;
    }

    @Override
    public void onAttachedToRecyclerView(RecyclerView recyclerView) {
        super.onAttachedToRecyclerView(recyclerView);
    }

    @Override
    public SearchViewHolder onCreateViewHolder(ViewGroup viewGroup, int i) {
        View view = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_searchresult, viewGroup, false);
        SearchViewHolder languageViewHolder = new SearchViewHolder(view);
        return languageViewHolder;
    }

    @Override
    public void onBindViewHolder(SearchViewHolder searchViewHolder, int i) {
        String timeInfo = searchResults.get(i).startTime + " - " + searchResults.get(i).endTime
                + " (" + searchResults.get(i).durationMinutes + "min)";
        String routeInfo = searchResults.get(i).startPosition + " to " + searchResults.get(i).endPosition;
        searchViewHolder.timeInfo.setText(timeInfo);
        searchViewHolder.routeInfo.setText(routeInfo);
        //TODO: check if getTimeToDeparture() is less than 30 minutes
        if(searchResults.get(i).isCurrent()){
            searchViewHolder.hurryAlertIcon.setVisibility(View.VISIBLE);
        }
    }

    @Override
    public int getItemCount() {
        return searchResults.size();
    }
}
