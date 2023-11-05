# coding: utf-8
import cupy as cp

def _numerical_gradient_1d(f, x):
    h = 1e-4 # 0.0001
    grad = cp.zeros_like(x)
    
    for idx in range(x.size):
        tmp_val = x[idx]
        x[idx] = float(tmp_val) + h
        fxh1 = f(x) # f(x+h)
        
        x[idx] = tmp_val - h 
        fxh2 = f(x) # f(x-h)
        grad[idx] = (fxh1 - fxh2) / (2*h)
        
        x[idx] = tmp_val # 値を元に戻す
        
    return grad


def numerical_gradient_2d(f, X):
    if X.ndim == 1:
        return _numerical_gradient_1d(f, X)
    else:
        grad = cp.zeros_like(X)
        
        for idx, x in enumerate(X):
            grad[idx] = _numerical_gradient_1d(f, x)
        
        return grad



def numerical_gradient(f, x):
    h = 1e-4 # 0.0001
    grad = cp.zeros_like(x)
    
    # x.ravel() で x の全要素にアクセスするための1次元表現を取得します。
    # これによってマルチインデックスの必要がなくなります。
    x_flat = x.ravel()
    grad_flat = grad.ravel()
    
    for idx in range(x_flat.size):
        tmp_val = x_flat[idx].get()  # .get() でスカラー値を取得します。
        x_flat[idx] = tmp_val + h
        fxh1 = f(x)  # f(x+h)
        
        x_flat[idx] = tmp_val - h
        fxh2 = f(x)  # f(x-h)
        grad_flat[idx] = (fxh1 - fxh2) / (2 * h)
        
        x_flat[idx] = tmp_val  # 値を元に戻します。
    
    # grad_flat を grad の形状に戻します。
    grad = grad_flat.reshape(x.shape)

    return grad
