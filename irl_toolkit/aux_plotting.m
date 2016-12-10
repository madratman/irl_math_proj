colormap(jet)
foldername='../outputs_toolkit/';
for i=1:10
    imagesc(-costMap{i});
    name=num2str(i-1,'%02d');
    print(strcat(foldername,name,'_costMap_orig'),'-dpng');
    contour(-costMap{i});
    print(strcat(foldername,name,'_countourMap_orig'),'-dpng');
end

wAvg=zeros(size(w_vec{1}));
for i=1:10
    wAvg=wAvg+w_vec{i};
end
wAvg=wAvg/10;

costMapAvg=cell(0);
for i=1:10
    costMapAvg{i}=wAvg'*featuresMap{i}';
    costMapAvg{i}=reshape(costMapAvg{i},100,100);
    name=num2str(i-1,'%02d');
    imagesc(-costMapAvg{i});
    print(strcat(foldername,name,'_costMap_avg'),'-dpng');
    contour(-costMapAvg{i});
    print(strcat(foldername,name,'_countourMap_avg'),'-dpng');
end

save('../outputs_toolkit/variables','costMap','costMapAvg','featuresMap','w_vec','wAvg');
