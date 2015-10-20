package se.uu.csproject.monadclient.recyclerviews;

import android.graphics.Color;
import android.os.CountDownTimer;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.RatingBar;
import android.widget.TextView;

import java.text.DecimalFormat;
import java.util.List;

import se.uu.csproject.monadclient.R;

import static java.lang.Math.floor;

public class TripRecyclerViewAdapter extends RecyclerView.Adapter<TripRecyclerViewAdapter.TripViewHolder>{

    public static class TripViewHolder extends RecyclerView.ViewHolder {

        TextView origin;
        TextView destination;
        TextView departureTime;
        TextView arrivalTime;
        TextView countdownTime; //active trips only
        TextView date;
        RatingBar feedback; // past trips only
        ImageView clockIcon;


        TripViewHolder(View itemView) {
            super(itemView);
            origin = (TextView) itemView.findViewById(R.id.label_origin);
            destination = (TextView) itemView.findViewById(R.id.label_destination);
            departureTime = (TextView) itemView.findViewById(R.id.label_departuretime);
            arrivalTime = (TextView) itemView.findViewById(R.id.label_arrivaltime);
            countdownTime = (TextView) itemView.findViewById(R.id.label_countdown);
            date = (TextView) itemView.findViewById(R.id.label_date);
            feedback = (RatingBar) itemView.findViewById(R.id.ratingbar);
            clockIcon = (ImageView) itemView.findViewById(R.id.icon_clock);
        }
    }

    @Override
    public int getItemViewType(int position) {
        if(trips.get(position).isCurrent()) {
            return 1;
        }
        else {
            return 0;
        }
    }

    List<Trip> trips;

    public TripRecyclerViewAdapter(List<Trip> trips){
        this.trips = trips;
    }

    @Override
    public void onAttachedToRecyclerView(RecyclerView recyclerView) {
        super.onAttachedToRecyclerView(recyclerView);
    }

    @Override
    public TripViewHolder onCreateViewHolder(ViewGroup viewGroup, int viewType) {
        View view;
        if(viewType == 1) {
            view = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_trips_active, viewGroup, false);
        }
        else {
            view = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_trips_past, viewGroup, false);
        }
        return new TripViewHolder(view);
    }

    @Override
    public void onBindViewHolder(final TripViewHolder tripViewHolder, int i) {
        tripViewHolder.origin.setText(trips.get(i).startPosition);
        tripViewHolder.destination.setText(trips.get(i).endPosition);
        tripViewHolder.departureTime.setText(trips.get(i).startTime);
        tripViewHolder.arrivalTime.setText(trips.get(i).endTime);

        if(trips.get(i).isCurrent()) {
            final long MILLISECONDS_TO_DEPARTURE = trips.get(i).getTimeToDeparture();
            final int MILLISECONDS = 1000;

            tripViewHolder.countdownTime.setText(formatCoundownText(MILLISECONDS_TO_DEPARTURE));
            // TODO: derive date from the attribute "startTime" in object Trip, format: "EEE dd MMM."
            tripViewHolder.date.setText("TODAY");

            //TODO (low priority): change parseColor() calls into theme colors
            CountDownTimer timer = new CountDownTimer(MILLISECONDS_TO_DEPARTURE, MILLISECONDS) {
                @Override
                public void onTick(long millisUntilFinished) {
                    tripViewHolder.countdownTime.setText(formatCoundownText(millisUntilFinished));
                    if (millisUntilFinished < 10000) {
                        tripViewHolder.countdownTime.setTextColor(Color.parseColor("#f44336"));
                        tripViewHolder.date.setTextColor(Color.parseColor("#f44336"));
                        tripViewHolder.clockIcon.setVisibility(View.VISIBLE);
                    }
                }

                @Override
                public void onFinish() {
                    tripViewHolder.countdownTime.setText("Trip in Progress");
                    tripViewHolder.countdownTime.setTextColor(Color.parseColor("#2e7d32"));
                    tripViewHolder.date.setTextColor(Color.parseColor("#2e7d32"));
                    tripViewHolder.clockIcon.setVisibility(View.INVISIBLE);
                    //tripViewHolder.clockIcon.setColorFilter(Color.parseColor("#2e7d32"));
                }
            }.start();
        }
        else {
            tripViewHolder.feedback.setRating(trips.get(i).userFeedback);
        }
    }

    @Override
    public int getItemCount() {
        return trips.size();
    }

    private String formatCoundownText(long millisecondsTime){
        DecimalFormat formatter = new DecimalFormat("00");
        String hours = formatter.format( floor(millisecondsTime / (1000 * 60 * 60)) );
        millisecondsTime %= (1000*60*60);
        String minutes = formatter.format( floor(millisecondsTime / (1000*60)) );
        millisecondsTime %= (1000*60);
        String seconds = formatter.format( floor(millisecondsTime / 1000) );
        return hours + ":" + minutes + ":" + seconds;
    }
}

