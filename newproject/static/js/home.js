$(function () {
//轮播图开始
        //点击下一张
        var index=0;
        $('#next').click(function () {
            index++;
            if (index===4){
                index=0;
            }
            $('.picBox li').eq(index).fadeIn(500).siblings().fadeOut(500)
            $('.circles span').eq(index).css('boxShadow','0 0 10px 5px rgba(0,0,0,.7) inset').siblings().css('boxShadow','none')
        });
        //点击上一张
        $('#prev').click(function () {
            index--;
            if (index===-1){
                index=3;
            }
            $('.picBox li').eq(index).fadeIn(500).siblings().fadeOut(500)
            $('.circles span').eq(index).css('boxShadow','0 0 10px 5px rgba(0,0,0,.7) inset').siblings().css('boxShadow','none')
        });
        //随时间自动切换
        function play() {
            timer=setInterval(function () {
                $('#next').click()
            },2000)
        }
        play();
        $('.Photo-frame').mouseover(function () {
            clearInterval(timer)
        })
        $('.Photo-frame').mouseout(function () {
            play()
        });
        //鼠标移入小圆点显示对应的图片
        $('.circles span').mouseover(function () {
            index=this.getAttribute('ind');
            $('.circles span').eq(index).css('boxShadow','0 0 10px 5px rgba(0,0,0,.7) inset').siblings().css('boxShadow','none');
            $('.picBox li').eq(index).fadeIn(500).siblings().fadeOut(500)
        })
//轮播图结束
})
//医院选择开始
window.onload=function() {
    var TitleLis = document.querySelectorAll('.tab-title li')//获取类名为title的ul中的li，结果为数组
    var BodyLis = document.querySelectorAll('.tab-body li')//获取类名为body的ul中的li，结果为数组
    // console.log(TitleLis,BodyLis)
    for (var i = 0; i < TitleLis.length; i++) {
        TitleLis[i].setAttribute('index', i)//将小li在数组中的下标标记为index
        TitleLis[i].onmouseover = function () {//鼠标移入上面四个小li时执行
            var index = this.getAttribute('index')//将小li的下标保存
            // console.log(index)
            for (var j = 0; j < BodyLis.length; j++) {
                TitleLis[j].style.backgroundColor = '#9ff3ff'//将所有小li的背景色变回蓝色
                BodyLis[j].style.display = "none"//将所有大li隐藏
            }
            TitleLis[index].style.backgroundColor = '#5eb0ff'//改变下标为index的小li的颜色
            BodyLis[index].style.display = 'block'//显示下标为index的大li
        }
    }
}
//医院选择结束