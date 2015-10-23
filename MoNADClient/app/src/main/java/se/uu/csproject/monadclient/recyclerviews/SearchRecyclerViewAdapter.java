package se.uu.csproject.monadclient.recyclerviews;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.List;

import se.uu.csproject.monadclient.R;
import se.uu.csproject.monadclient.RouteActivity;

public class SearchRecyclerViewAdapter extends RecyclerView.Adapter<SearchRecyclerViewAdapter.SearchViewHolder>{

    public static class SearchViewHolder extends RecyclerView.ViewHolder {

        TextView timeInfo;
        TextView routeInfo;
        ImageView hurryAlertIcon;
        ImageButton tripInfoButton;

        SearchViewHolder(View itemView) {
            super(itemView);
            timeInfo = (TextView) itemView.findViewById(R.id.label_timeinfo);
            routeInfo = (TextView) itemView.findViewById(R.id.label_routeinfo);
            hurryAlertIcon = (ImageView) itemView.findViewById(R.id.icon_hurry);
            tripInfoButton = (ImageButton) itemView.findViewById(R.id.button_tripdetails);
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
    public void onBindViewHolder(final SearchViewHolder searchViewHolder, final int i) {
        String timeInfo = searchResults.get(i).getStartTime() + " - " + searchResults.get(i).getEndTime()
                + " (" + searchResults.get(i).getDurationMinutes() + "min)";
        String routeInfo = searchResults.get(i).getStartPosition() + " to " + searchResults.get(i).getEndPosition();
        searchViewHolder.timeInfo.setText(timeInfo);
        searchViewHolder.routeInfo.setText(routeInfo);
        //TODO: check if getTimeToDeparture() is less than 30 minutes
        if(searchResults.get(i).isCurrent()){
            searchViewHolder.hurryAlertIcon.setVisibility(View.VISIBLE);
        }

        searchViewHolder.tripInfoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(searchViewHolder.itemView.getContext(), RouteActivity.class);
                Bundle bundle = new Bundle();
                bundle.putInt("tripId", searchResults.get(i).getTripId());
                bundle.putString("startPosition", searchResults.get(i).getStartPosition());
                bundle.putString("endPosition", searchResults.get(i).getEndPosition());
                bundle.putString("startTime", searchResults.get(i).getStartTime());
                bundle.putString("endTime", searchResults.get(i).getEndTime());
                bundle.putInt("duration", searchResults.get(i).getDurationMinutes());
                intent.putExtras(bundle);
                searchViewHolder.itemView.getContext().startActivity(intent);
            }
        });
    }

    @Override
    public int getItemCount() {
        return searchResults.size();
    }
}
