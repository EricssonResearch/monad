package se.uu.csproject.monadclient.recyclerviews;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.support.v4.app.NotificationCompat;
import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;

import se.uu.csproject.monadclient.NotificationsActivity;
import se.uu.csproject.monadclient.R;
import se.uu.csproject.monadclient.RouteActivity;
import se.uu.csproject.monadclient.SearchActivity;

public class NotificationRecyclerViewAdapter extends RecyclerView.Adapter<NotificationRecyclerViewAdapter.NotificationViewHolder> {


    List<Notify> notify;
    private Context mContext;
    ArrayList<FullTrip> bookings;


    public NotificationRecyclerViewAdapter(Context context, List<Notify> notify, ArrayList<FullTrip> bookings) {
        this.notify = notify;
        mContext = context;
        this.bookings = bookings;
    }


    @Override
    public int getItemViewType(int position) {
        if (notify.get(position).isToday()) {

            if (notify.get(position).reschedule) {
                return 2;
            } else {
                return 1;
            }
        } else {
            return 0;
        }
    }

    @Override
    public void onAttachedToRecyclerView(RecyclerView recyclerView) {
        super.onAttachedToRecyclerView(recyclerView);
    }

    @Override
    public NotificationViewHolder onCreateViewHolder(ViewGroup viewGroup, int viewType) {
        View view;
        if (viewType == 2) {
            view = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_notification_reschedule, viewGroup, false);

        } else if (viewType == 1) {
            view = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_notification, viewGroup, false);

        } else {
            view = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_notification_old, viewGroup, false);

        }

        return new NotificationViewHolder(mContext, view);

    }


    @Override
    public void onBindViewHolder(final NotificationViewHolder notificationViewHolder, final int i) {
        notificationViewHolder.notificationTime.setText(formatTime((Date) notify.get(i).time, notify.get(i).isToday()));

        notificationViewHolder.notificationPhoto.setImageResource(notify.get(i).iconID);
        notificationViewHolder.notificationPhoto.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                FullTrip fullTrip = getTrip(notify.get(i).getTripID());
                if (fullTrip != null) {
                    Intent intent = new Intent(notificationViewHolder.itemView.getContext(), RouteActivity.class);
                    intent.putExtra("selectedTrip", fullTrip);
                    notificationViewHolder.itemView.getContext().startActivity(intent);
                } else {
                    System.out.println("Trip is not in bookings list");

                }
            }

        });

        notificationViewHolder.notificationText.setText(notify.get(i).text);
        notificationViewHolder.notificationText.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                FullTrip fullTrip = getTrip(notify.get(i).getTripID());

                if (fullTrip != null) {
                    Intent intent = new Intent(notificationViewHolder.itemView.getContext(), RouteActivity.class);
                    intent.putExtra("selectedTrip", fullTrip);
                    notificationViewHolder.itemView.getContext().startActivity(intent);
                } else {
                    System.out.println("Trip is not in bookings list");

                }
            }
        });

        notificationViewHolder.hideNotificationButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                notificationViewHolder.itemView.setVisibility(View.GONE);
//                int index = notify.indexOf(i);

                Storage.removeNotification(i);
                notify = Storage.getNotifications();
//                notifyItemRemoved(index);
                notifyDataSetChanged();
            }
        });

        if (getItemViewType(i) == 2) {
            notificationViewHolder.rescheduleText.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    FullTrip fullTrip = getTrip(notify.get(i).getTripID());
                    if (fullTrip != null) {
                        Intent intent = new Intent(notificationViewHolder.itemView.getContext(), SearchActivity.class);
                        intent.putExtra("selectedTrip", fullTrip);
                        notificationViewHolder.itemView.getContext().startActivity(intent);
                    } else {
                        System.out.println("Trip is not in bookings list");

                    }
                }

            });
        }

    }

    @Override
    public int getItemCount() {
        return notify.size();
    }


    public static class NotificationViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {

        Context mContext;
        CardView cv;
        TextView notificationText;
        TextView rescheduleText; //only for reschedule notifications
        TextView notificationTime;
        ImageView notificationPhoto;
        ImageView notificationImage;
        int numMessages = 0;
        ImageView hideNotificationButton;


        NotificationViewHolder(Context context, View itemView) {

            super(itemView);
            mContext = context;
            cv = (CardView) itemView.findViewById(R.id.cv);
            notificationText = (TextView) itemView.findViewById(R.id.label_text);
            rescheduleText = (TextView) itemView.findViewById(R.id.label_reschedule);
            notificationTime = (TextView) itemView.findViewById(R.id.label_time);
            notificationPhoto = (ImageView) itemView.findViewById(R.id.label_icon);
            notificationImage = (ImageView) itemView.findViewById(R.id.image1);
            hideNotificationButton = (ImageView) itemView.findViewById(R.id.image2);
            notificationImage.setOnClickListener(this);
            hideNotificationButton.setOnClickListener(this);
            itemView.setOnClickListener(this);
            itemView.setTag(itemView);
        }


        public void onClick(View v) {

            if (v.getId() == R.id.image1) {
                Intent allNotesIntent = new Intent(mContext, NotificationsActivity.class);
                allNotesIntent.putExtra(NotificationsActivity.NOTIFICATION_ID_STR, NotificationsActivity.NOTIFICATION_ID);
                PendingIntent allNotesPendingIntent = PendingIntent.getActivity(mContext, 0, allNotesIntent, PendingIntent.FLAG_CANCEL_CURRENT);
                NotificationCompat.Builder mBuilder;
                mBuilder = new NotificationCompat.Builder(mContext);
                mBuilder.setSmallIcon(R.mipmap.ic_launcher);
                mBuilder.setContentTitle(mContext.getString(R.string.label_notification_notification));
                mBuilder.setContentText(notificationText.getText());
                mBuilder.setAutoCancel(true);
                mBuilder.setContentText(this.itemView.getResources().getString(R.string.java_notificationsrva_newmessages))
                        .setNumber(++numMessages);

                NotificationManager mNotificationManager = (NotificationManager)
                        mContext.getSystemService(Context.NOTIFICATION_SERVICE);

                mNotificationManager.notify(NotificationsActivity.NOTIFICATION_ID, mBuilder.build());
            }


        }
    }

    private String formatTime(Date date, boolean today) {

        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        String time;

        if (today) {
            long timeDifference = Calendar.getInstance().getTimeInMillis() - calendar.getTimeInMillis();
            time = formatTodayTime(timeDifference);
        } else {
            SimpleDateFormat timeFormat = new SimpleDateFormat("MM/dd");
            time = timeFormat.format(calendar.getTime());
        }
        return time;
    }

    private String formatTodayTime(long millisecondsTime) {

        millisecondsTime %= (1000 * 60 * 60 * 24);
        int hours = (int) millisecondsTime / (1000 * 60 * 60);
        millisecondsTime %= (1000 * 60 * 60);
        int minutes = (int) millisecondsTime / (1000 * 60);
        millisecondsTime %= (1000 * 60);
        int seconds = (int) millisecondsTime / 1000;
        if (minutes == 0) {
            return seconds + " sec ago";
        } else if (hours == 0) {
            return minutes + " min ago";
        } else if (hours == 1) {
            return hours + " hr, " + minutes + "ago";
        } else {
            return hours + " hrs ago";
        }
    }

// Start of a loop that processes data and then notifies the user


    // Because the ID remains unchanged, the existing notification is
    // updated.

    private FullTrip getTrip(String id) {

        for (int i = 0; i < bookings.size(); i++) {
            if (bookings.get(i).getId().equals(id)) {
                return bookings.get(i);
            }
        }
        return null;
    }
}