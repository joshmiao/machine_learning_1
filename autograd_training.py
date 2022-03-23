import torch
import time
import os
import model_evaluate


def train(x_tlist, y_tlist, theta, theta_num, dict_size, epoch, learning_rate, device):
    if len(x_tlist) != len(y_tlist):
        print('Data error!')
    training_cnt = len(x_tlist) // 5 * 4
    print('Initial theta : ')
    print(theta)
    print('-------------------------------------------------------------------------------------------------------')
    for __epoch__idx__ in range(epoch):
        print("epoch :", __epoch__idx__)
        st_time = time.time()
        # using softmax model to optimize theta #
        li = torch.tensor(0, device=device, dtype=torch.float32)
        for idx in range(training_cnt):
            sigma = torch.tensor(1, device=device, dtype=torch.float32)
            for i in range(2):
                sigma += torch.exp(theta[i] @ x_tlist[idx])
            sigma = torch.log(sigma)
            li -= sigma
            if y_tlist[idx][theta_num] != 2:
                li += theta[y_tlist[idx][theta_num]] @ x_tlist[idx]
        li /= training_cnt
        li.backward(gradient=torch.tensor(1, dtype=torch.float32, device=device))
        with torch.no_grad():
            theta += learning_rate * theta.grad
            theta.grad = None
        # using softmax model to optimize theta #
        print('li = ', li)
        print(theta)
        print('Used time = {0:} second(s)'.format(time.time() - st_time))
        precision_rate, recall_rate, f1_measure = model_evaluate.evaluate_model(x_tlist=x_tlist, y_tlist=y_tlist,
                                                                                start=training_cnt, end=len(x_tlist),
                                                                                theta=theta, theta_num=theta_num)
        print('---------------------------------------------------------------------------------------------------')
        if not os.path.exists('./theta{}_save/'.format(theta_num)):
            os.mkdir('./theta{}_save/'.format(theta_num))
        torch.save(theta,
                   './theta_save/theta{0:}_save_tmp_{1:}_dic_size={2:}_F1={3:.4f}_li={4:.4f}.pt'
                   .format(theta_num, __epoch__idx__, dict_size, f1_measure, li.item()))