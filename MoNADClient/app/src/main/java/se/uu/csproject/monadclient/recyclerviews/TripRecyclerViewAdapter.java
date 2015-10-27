package se.uu.csproject.monadclient.recyclerviews;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.RatingBar;
import android.widget.TextView;

import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import se.uu.csproject.monadclient.R;
import se.uu.csproject.monadclient.RouteActivity;
import se.uu.csproject.monadclient.TripCancelPopup;

import static java.lang.Math.floor;

public class TripRecyclerViewAdapter
        extends RecyclerView.Adapter<TripRecyclerViewAdapter.TripViewHolder>{

    List<Trip> trips;

    public class TripViewHolder extends RecyclerView.ViewHolder {

        TextView origin;
        TextView destination;
        TextView departureTime;
        TextView arrivalTime;
        TextView date;
        ImageView clockIcon;
        TextView countdownTime; //active trips only
        ImageButton routeInfoButton; //active trips only
        ImageButton cancelButton; //active trips only
        RatingBar feedback; // past trips only

        TripViewHolder(final View itemView) {
            super(itemView);
            origin = (TextView) itemView.findViewById(R.id.label_origin);
            destination = (TextView) itemView.findViewById(R.id.label_destination);
            departureTime = (TextView) itemView.findViewById(R.id.label_departuretime);
            arrivalTime = (TextView) itemView.findViewById(R.id.label_arrivaltime);
            countdownTime = (TextView) itemView.findViewById(R.id.label_countdown);
            date = (TextView) itemView.findViewById(R.id.label_date);
            feedback = (RatingBar) itemView.findViewById(R.id.ratingbar);
            clockIcon = (ImageView) itemView.findViewById(R.id.icon_clock);
            routeInfoButton = (ImageButton) itemView.findViewById(R.id.button_routeinfo);
            cancelButton = (ImageButton) itemView.findViewById(R.id.cancel);
        }
    }

    @Override
    public int getItemViewType(int position) {
        if(trips.get(position).isHistory()) {
            return 0;
        }
        else {
            return 1;
        }
    }

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
    public void onBindViewHolder(final TripViewHolder tripViewHolder, final int i) {
        tripViewHolder.origin.setText(trips.get(i).getStartBusStop());
        tripViewHolder.destination.setText(trips.get(i).getEndBusStop());
        tripViewHolder.departureTime.setText(formatTime(trips.get(i).getStartTime()));
        tripViewHolder.arrivalTime.setText(formatTime(trips.get(i).getEndTime()));

        final int MILLISECONDS = 1000;

        //if the trip is active (happening or not happened yet)
        if(!trips.get(i).isHistory()) {
            if(trips.get(i).isInProgress()){
                formatAsInProgress(tripViewHolder);
            }
            else{
                if(trips.get(i).isToday()){
                    tripViewHolder.date.setText("TODAY");
                    tripViewHolder.date.setTextColor(Color.parseColor("#f44336"));
                }
                else {
                    tripViewHolder.date.setText(formatDate(trips.get(i).getStartTime()));
                }

                final long MILLISECONDS_TO_DEPARTURE = trips.get(i).getTimeToDeparture();
                tripViewHolder.countdownTime.setText(formatCountdownText(MILLISECONDS_TO_DEPARTURE));

                //TODO (low priority): change parseColor() calls into theme colors
                CountDownTimer timer = new CountDownTimer(MILLISECONDS_TO_DEPARTURE, MILLISECONDS) {
                    @Override
                    public void onTick(long millisUntilFinished) {
                        tripViewHolder.countdownTime.setText(formatCountdownText(millisUntilFinished));
                        //change value to 30min (30*60*1000 = 1 800 000ms)
                        if (millisUntilFinished < 1800000) {
                            tripViewHolder.countdownTime.setTextColor(Color.parseColor("#f44336"));
                            tripViewHolder.clockIcon.setVisibility(View.VISIBLE);
                        }
                    }

                    @Override
                    public void onFinish() {
                        formatAsInProgress(tripViewHolder);
                    }
                }.start();
            }

           tripViewHolder.routeInfoButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(tripViewHolder.itemView.getContext(), RouteActivity.class);
                    Bundle bundle = new Bundle();
                    bundle.putInt("tripId", trips.get(i).getTripId());
                    bundle.putString("startBusStop", trips.get(i).getStartBusStop());
                    bundle.putString("endBusStop", trips.get(i).getEndBusStop());
                    bundle.putSerializable("startTime", trips.get(i).getStartTime());
                    bundle.putSerializable("endTime", trips.get(i).getEndTime());
                    bundle.putInt("duration", trips.get(i).getDurationMinutes());
                    intent.putExtras(bundle);
                    tripViewHolder.itemView.getContext().startActivity(intent);
                }
           });

            tripViewHolder.cancelButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(tripViewHolder.itemView.getContext(), TripCancelPopup.class);
                    Bundle bundle = new Bundle();
                    bundle.putInt("tripId", trips.get(i).getTripId());
                    bundle.putString("startBusStop", trips.get(i).getStartBusStop());
                    bundle.putString("endBusStop", trips.get(i).getEndBusStop());
                    bundle.putSerializable("startTime", trips.get(i).getStartTime());
                    bundle.putSerializable("endTime", trips.get(i).getEndTime());
                    bundle.putInt("MILLISECONDS", MILLISECONDS);
                    bundle.putInt("duration", trips.get(i).getDurationMinutes());
                    bundle.putInt("feedback", trips.get(i).getUserFeedback());
                    intent.putExtras(bundle);
                    tripViewHolder.itemView.getContext().startActivity(intent);
                }
            });
        }
        // if the trip already happened
        else {
            tripViewHolder.feedback.setRating(trips.get(i).getUserFeedback());
        }
    }

    @Override
    public int getItemCount() {
        return trips.size();
    }

    private String formatCountdownText(long millisecondsTime){
        DecimalFormat formatter = new DecimalFormat("00");
        String days = formatter.format(floor(millisecondsTime / (1000 * 60 * 60 * 24)));
        millisecondsTime %= (1000*60*60*24);
        String hours = formatter.format( floor(millisecondsTime / (1000 * 60 * 60)) );
        millisecondsTime %= (1000*60*60);
        String minutes = formatter.format( floor(millisecondsTime / (1000*60)) );
        millisecondsTime %= (1000*60);
        String seconds = formatter.format( floor(millisecondsTime / 1000) );
        if(days.equals("00")){
            return hours + ":" + minutes + ":" + seconds;
        }
        else if(days.equals("01")){
            return days + " day, " + hours + ":" + minutes + ":" + seconds;
        }
        else{
            return days + " day(s), " + hours + ":" + minutes + ":" + seconds;
        }
    }

    private void formatAsInProgress(TripViewHolder tripViewHolder) {
        tripViewHolder.date.setText("TODAY");
        tripViewHolder.countdownTime.setText("Trip in Progress");
        tripViewHolder.countdownTime.setTextColor(Color.parseColor("#2e7d32"));
        tripViewHolder.date.setTextColor(Color.parseColor("#2e7d32"));
        tripViewHolder.clockIcon.setVisibility(View.INVISIBLE);
        //tripViewHolder.clockIcon.setColorFilter(Color.parseColor("#2e7d32"));
    }

    private String formatTime(Date date){
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        return timeFormat.format(calendar.getTime());
    }

    private String formatDate(Date date){
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        SimpleDateFormat dateFormat = new SimpleDateFormat("EEE dd MMM.");
        return dateFormat.format(calendar.getTime());
    }
}