package se.uu.csproject.monadclient.recyclerviews;

import android.content.Intent;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.Calendar;
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

    List<FullTrip> searchResults;

    public SearchRecyclerViewAdapter(List<FullTrip> searchResults){
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
        String routeInfo = searchResults.get(i).getStartBusStop() + " to " + searchResults.get(i).getEndBusStop();
        searchViewHolder.timeInfo.setText(formatTripTime(searchResults.get(i)));
        searchViewHolder.routeInfo.setText(routeInfo);
        //TODO: check if getTimeToDeparture() is less than 30 minutes
        if(!searchResults.get(i).isHistory() && searchResults.get(i).getTimeToDeparture() < 1800000){
            searchViewHolder.hurryAlertIcon.setVisibility(View.VISIBLE);
        }

        searchViewHolder.tripInfoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(searchViewHolder.itemView.getContext(), RouteActivity.class);
                intent.putExtra("fulltrip", searchResults.get(i));
                searchViewHolder.itemView.getContext().startActivity(intent);
            }
        });
    }

    @Override
    public int getItemCount() {
        return searchResults.size();
    }

    private String formatTripTime(FullTrip fulltrip){

        Calendar calendar = Calendar.getInstance();
        calendar.setTime(fulltrip.getStartTime());
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        String startTime = timeFormat.format(calendar.getTime());
        calendar.setTime(fulltrip.getEndTime());
        String endTime = timeFormat.format(calendar.getTime());

        String timeInfo = startTime + " - " + endTime + " (" +
                fulltrip.getDuration() + "min)";
        return timeInfo;
    }
}
