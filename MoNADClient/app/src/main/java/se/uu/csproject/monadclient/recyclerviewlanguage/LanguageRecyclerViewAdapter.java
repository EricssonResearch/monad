package se.uu.csproject.monadclient.recyclerviewlanguage;

import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.List;

import se.uu.csproject.monadclient.R;

public class LanguageRecyclerViewAdapter extends RecyclerView.Adapter<LanguageRecyclerViewAdapter.LanguageViewHolder>{

    public static class LanguageViewHolder extends RecyclerView.ViewHolder {

        ImageView languageFlag;
        TextView languageName;

        LanguageViewHolder(View itemView) {
            super(itemView);
            languageFlag = (ImageView) itemView.findViewById(R.id.icon_flag);
            languageName = (TextView) itemView.findViewById(R.id.label_language);
        }
    }

    List<Language> languages;

    public LanguageRecyclerViewAdapter(List<Language> languages){
        this.languages = languages;
    }

    @Override
    public void onAttachedToRecyclerView(RecyclerView recyclerView) {
        super.onAttachedToRecyclerView(recyclerView);
    }

    @Override
    public LanguageViewHolder onCreateViewHolder(ViewGroup viewGroup, int i) {
        View view = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_language, viewGroup, false);
        LanguageViewHolder languageViewHolder = new LanguageViewHolder(view);
        return languageViewHolder;
    }

    @Override
    public void onBindViewHolder(LanguageViewHolder personViewHolder, int i) {
        personViewHolder.languageName.setText(languages.get(i).name);
        personViewHolder.languageFlag.setImageResource(languages.get(i).flagId);
    }

    @Override
    public int getItemCount() {
        return languages.size();
    }
}
