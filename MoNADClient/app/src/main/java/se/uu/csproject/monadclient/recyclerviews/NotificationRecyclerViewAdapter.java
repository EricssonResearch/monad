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
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import se.uu.csproject.monadclient.NotificationsActivity;
import se.uu.csproject.monadclient.R;

public class NotificationRecyclerViewAdapter extends RecyclerView.Adapter<NotificationRecyclerViewAdapter.NotificationViewHolder> {


    List<Notify> notify;
    private Context mContext;

    public NotificationRecyclerViewAdapter(Context context, List<Notify> notify) {
        this.notify = notify;
        mContext = context;
    }

    @Override
    public void onAttachedToRecyclerView(RecyclerView recyclerView) {
        super.onAttachedToRecyclerView(recyclerView);
    }

    @Override
    public NotificationViewHolder onCreateViewHolder(ViewGroup viewGroup, int i) {
        View view = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_notification, viewGroup, false);
        return new NotificationViewHolder(mContext, view);

    }

    @Override
    public void onBindViewHolder(final NotificationViewHolder notificationViewHolder, final int i) {
        notificationViewHolder.notificationName.setText(notify.get(i).text);
        notificationViewHolder.notificationTime.setText(formatTime((Date) notify.get(i).time));
        notificationViewHolder.notificationPhoto.setImageResource(notify.get(i).iconId);

        notificationViewHolder.hideNotificationButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                notificationViewHolder.itemView.setVisibility(View.GONE);
            }
        });

    }

    @Override
    public int getItemCount() {
        return notify.size();
    }


    public static class NotificationViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {
        Context mContext;
        CardView cv;
        TextView notificationName;
        TextView notificationTime;
        ImageView notificationPhoto;
        ImageView notificationImage;
        int numMessages = 0;
        ImageView hideNotificationButton;


        NotificationViewHolder(Context context, View itemView) {
            super(itemView);
            mContext = context;
            cv = (CardView) itemView.findViewById(R.id.cv);
            notificationName = (TextView) itemView.findViewById(R.id.label_text);
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
                mBuilder.setContentText(notificationName.getText());
                mBuilder.setAutoCancel(true);
                mBuilder.setContentText("You've received new messages.")
                        .setNumber(++numMessages);

                NotificationManager mNotificationManager = (NotificationManager)
                        mContext.getSystemService(Context.NOTIFICATION_SERVICE);

                mNotificationManager.notify(NotificationsActivity.NOTIFICATION_ID, mBuilder.build());
            }



        }
    }

    private String formatTime(Date date){

        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        String time = timeFormat.format(calendar.getTime());

        return time;
    }

// Start of a loop that processes data and then notifies the user


    // Because the ID remains unchanged, the existing notification is
    // updated.

}




