document.addEventListener('DOMContentLoaded', () => {
  const toast = document.createElement('div');
  toast.id = 'copy-toast';
  toast.innerText = '复制成功!';
  document.body.appendChild(toast);

  document.querySelectorAll('code.literal').forEach(code => {
    const isLink = code.closest('a');
    code.title = isLink ? '左键复制，中键打开' : '复制到剪贴板';
    
    code.addEventListener('click', e => {
      if (isLink) e.preventDefault();
      navigator.clipboard.writeText(code.innerText).then(() => {
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 1000);
      });
    });
  });
});