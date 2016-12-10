python plot_learnt_reward.py weights_max_ent.txt data_test/0/all_final.pkl
mv reward_learnt.png results_final/0_max_ent_test_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data_test/1/all_final.pkl
mv reward_learnt.png results_final/1_max_ent_test_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data_test/2/all_final.pkl
mv reward_learnt.png results_final/2_max_ent_test_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data_test/3/all_final.pkl
mv reward_learnt.png results_final/3_max_ent_test_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data_test/4/all_final.pkl
mv reward_learnt.png results_final/4_max_ent_test_costmap.png

python plot_learnt_reward.py weights_avg_mmp.txt data_test/0/all_final.pkl
mv reward_learnt.png results_final/0_mmp_test_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data_test/1/all_final.pkl
mv reward_learnt.png results_final/1_mmp_test_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data_test/2/all_final.pkl
mv reward_learnt.png results_final/2_mmp_test_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data_test/3/all_final.pkl
mv reward_learnt.png results_final/3_mmp_test_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data_test/4/all_final.pkl
mv reward_learnt.png results_final/4_mmp_test_costmap.png

cp data_test/0/obstacles.png results_final/0_test_costmap.png
cp data_test/1/obstacles.png results_final/1_test_costmap.png
cp data_test/2/obstacles.png results_final/2_test_costmap.png
cp data_test/3/obstacles.png results_final/3_test_costmap.png
cp data_test/4/obstacles.png results_final/4_test_costmap.png

cp data/00/obstacles.png results_final/0_train_costmap.png
cp data/01/obstacles.png results_final/1_train_costmap.png
cp data/02/obstacles.png results_final/2_train_costmap.png
cp data/03/obstacles.png results_final/3_train_costmap.png
cp data/04/obstacles.png results_final/4_train_costmap.png
cp data/05/obstacles.png results_final/5_train_costmap.png
cp data/06/obstacles.png results_final/6_train_costmap.png
cp data/07/obstacles.png results_final/7_train_costmap.png
cp data/08/obstacles.png results_final/8_train_costmap.png
cp data/09/obstacles.png results_final/9_train_costmap.png

cp data/00/a_star_fake_experts_fixed.png results_final/0_train_traj.png
cp data/01/a_star_fake_experts_fixed.png results_final/1_train_traj.png
cp data/02/a_star_fake_experts_fixed.png results_final/2_train_traj.png
cp data/03/a_star_fake_experts_fixed.png results_final/3_train_traj.png
cp data/04/a_star_fake_experts_fixed.png results_final/4_train_traj.png
cp data/05/a_star_fake_experts_fixed.png results_final/5_train_traj.png
cp data/06/a_star_fake_experts_fixed.png results_final/6_train_traj.png
cp data/07/a_star_fake_experts_fixed.png results_final/7_train_traj.png
cp data/08/a_star_fake_experts_fixed.png results_final/8_train_traj.png
cp data/09/a_star_fake_experts_fixed.png results_final/9_train_traj.png

python plot_learnt_reward.py weights_avg_mmp.txt data/00/all_final.pkl
mv reward_learnt.png results_final/0_mmp_train_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data/01/all_final.pkl
mv reward_learnt.png results_final/1_mmp_train_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data/02/all_final.pkl
mv reward_learnt.png results_final/2_mmp_train_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data/03/all_final.pkl
mv reward_learnt.png results_final/3_mmp_train_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data/04/all_final.pkl
mv reward_learnt.png results_final/4_mmp_train_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data/05/all_final.pkl
mv reward_learnt.png results_final/5_mmp_train_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data/06/all_final.pkl
mv reward_learnt.png results_final/6_mmp_train_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data/07/all_final.pkl
mv reward_learnt.png results_final/7_mmp_train_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data/08/all_final.pkl
mv reward_learnt.png results_final/8_mmp_train_costmap.png
python plot_learnt_reward.py weights_avg_mmp.txt data/09/all_final.pkl
mv reward_learnt.png results_final/9_mmp_train_costmap.png

python plot_learnt_reward.py weights_max_ent.txt data/00/all_final.pkl
mv reward_learnt.png results_final/0_max_ent_train_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data/01/all_final.pkl
mv reward_learnt.png results_final/1_max_ent_train_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data/02/all_final.pkl
mv reward_learnt.png results_final/2_max_ent_train_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data/03/all_final.pkl
mv reward_learnt.png results_final/3_max_ent_train_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data/04/all_final.pkl
mv reward_learnt.png results_final/4_max_ent_train_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data/05/all_final.pkl
mv reward_learnt.png results_final/5_max_ent_train_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data/06/all_final.pkl
mv reward_learnt.png results_final/6_max_ent_train_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data/07/all_final.pkl
mv reward_learnt.png results_final/7_max_ent_train_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data/08/all_final.pkl
mv reward_learnt.png results_final/8_max_ent_train_costmap.png
python plot_learnt_reward.py weights_max_ent.txt data/09/all_final.pkl
mv reward_learnt.png results_final/9_max_ent_train_costmap.png

cd results_final
find . -name "*.png" -exec convert {} -trim {} \;
find . -name "*.png" -exec convert {} -resize 400X400! -quality 100 {} \;
find . -name "*.png" -exec convert {} -trim {} \;

montage 0_train_costmap.png 0_mmp_train_costmap.png 0_max_ent_train_costmap.png -tile 3x1 -geometry +1+1 montage_train_0.png
montage 1_train_costmap.png 1_mmp_train_costmap.png 1_max_ent_train_costmap.png -tile 3x1 -geometry +1+1 montage_train_1.png
montage 2_train_costmap.png 2_mmp_train_costmap.png 2_max_ent_train_costmap.png -tile 3x1 -geometry +1+1 montage_train_2.png
montage 3_train_costmap.png 3_mmp_train_costmap.png 3_max_ent_train_costmap.png -tile 3x1 -geometry +1+1 montage_train_3.png
montage 4_train_costmap.png 4_mmp_train_costmap.png 4_max_ent_train_costmap.png -tile 3x1 -geometry +1+1 montage_train_4.png
montage 5_train_costmap.png 5_mmp_train_costmap.png 5_max_ent_train_costmap.png -tile 3x1 -geometry +1+1 montage_train_5.png
montage 6_train_costmap.png 6_mmp_train_costmap.png 6_max_ent_train_costmap.png -tile 3x1 -geometry +1+1 montage_train_6.png
montage 7_train_costmap.png 7_mmp_train_costmap.png 7_max_ent_train_costmap.png -tile 3x1 -geometry +1+1 montage_train_7.png
montage 8_train_costmap.png 8_mmp_train_costmap.png 8_max_ent_train_costmap.png -tile 3x1 -geometry +1+1 montage_train_8.png
montage 9_train_costmap.png 9_mmp_train_costmap.png 9_max_ent_train_costmap.png -tile 3x1 -geometry +1+1 montage_train_9.png

montage 0_train_traj.png 0_train_costmap.png 0_mmp_train_costmap.png 0_max_ent_train_costmap.png -tile 4x1 -geometry +1+1 montage_train_0_with_traj.png
montage 1_train_traj.png 1_train_costmap.png 1_mmp_train_costmap.png 1_max_ent_train_costmap.png -tile 4x1 -geometry +1+1 montage_train_1_with_traj.png
montage 2_train_traj.png 2_train_costmap.png 2_mmp_train_costmap.png 2_max_ent_train_costmap.png -tile 4x1 -geometry +1+1 montage_train_2_with_traj.png
montage 3_train_traj.png 3_train_costmap.png 3_mmp_train_costmap.png 3_max_ent_train_costmap.png -tile 4x1 -geometry +1+1 montage_train_3_with_traj.png
montage 4_train_traj.png 4_train_costmap.png 4_mmp_train_costmap.png 4_max_ent_train_costmap.png -tile 4x1 -geometry +1+1 montage_train_4_with_traj.png
montage 5_train_traj.png 5_train_costmap.png 5_mmp_train_costmap.png 5_max_ent_train_costmap.png -tile 4x1 -geometry +1+1 montage_train_5_with_traj.png
montage 6_train_traj.png 6_train_costmap.png 6_mmp_train_costmap.png 6_max_ent_train_costmap.png -tile 4x1 -geometry +1+1 montage_train_6_with_traj.png
montage 7_train_traj.png 7_train_costmap.png 7_mmp_train_costmap.png 7_max_ent_train_costmap.png -tile 4x1 -geometry +1+1 montage_train_7_with_traj.png
montage 8_train_traj.png 8_train_costmap.png 8_mmp_train_costmap.png 8_max_ent_train_costmap.png -tile 4x1 -geometry +1+1 montage_train_8_with_traj.png
montage 9_train_traj.png 9_train_costmap.png 9_mmp_train_costmap.png 9_max_ent_train_costmap.png -tile 4x1 -geometry +1+1 montage_train_9_with_traj.png

montage 0_test_costmap.png 0_mmp_test_costmap.png 0_max_ent_test_costmap.png -tile 3x1 -geometry +1+1 montage_test_0.png
montage 1_test_costmap.png 1_mmp_test_costmap.png 1_max_ent_test_costmap.png -tile 3x1 -geometry +1+1 montage_test_1.png
montage 2_test_costmap.png 2_mmp_test_costmap.png 2_max_ent_test_costmap.png -tile 3x1 -geometry +1+1 montage_test_2.png
montage 3_test_costmap.png 3_mmp_test_costmap.png 3_max_ent_test_costmap.png -tile 3x1 -geometry +1+1 montage_test_3.png
montage 4_test_costmap.png 4_mmp_test_costmap.png 4_max_ent_test_costmap.png -tile 3x1 -geometry +1+1 montage_test_4.png

find . -name "*.png" -exec convert {} -trim {} \;
