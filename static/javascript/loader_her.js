var $body = document.body,
    $wrap = document.getElementById('wrap'),
    $maker = $('.maker'),

    areawidth = window.innerWidth,
    areaheight = window.innerHeight,

    canvassize = $maker.width(),

    length = 30,
    radius = 5.6,

    ringcolor = 0x5E4D89,

    rotatevalue = 0.035,
    acceleration = 0,
    animatestep = 0,
    toend = false,

    pi2 = Math.PI * 2,

    group = new THREE.Group(),
    mesh, ringcover, ring,

    camera, scene, renderer;

$('#wrap').css({
    'top': -$maker.width() / 2 + 50
    // toDo : 윈도우 사이즈에 따라 잘 안맞는데 이유 확인하고, 수식 개선.
});

camera = new THREE.PerspectiveCamera(65, 1, 1, 10000);
camera.position.z = 150;

scene = new THREE.Scene();
// scene.add(new THREE.AxisHelper(30));
scene.add(group);

mesh = new THREE.Mesh(
    new THREE.TubeGeometry(new (THREE.Curve.create(function () {
        },
        function (percent) {
            var x = length * Math.sin(pi2 * percent),
                y = radius * Math.cos(pi2 * 3 * percent),
                z, t;

            t = percent % 0.25 / 0.25;
            t = percent % 0.25 - (2 * (1 - t) * t * -0.0185 + t * t * 0.25);
            if (Math.floor(percent / 0.25) == 0 || Math.floor(percent / 0.25) == 2) {
                t *= -1;
            }
            z = radius * Math.sin(pi2 * 2 * (percent - t));

            return new THREE.Vector3(x, y, z);

        }
    ))(), 200, 1.1, 2, true),
    new THREE.MeshBasicMaterial({
        color: ringcolor   // 돌아가는 뱅글뱅글이의 색
        // , wireframe: true
    })
);
group.add(mesh);

// 다 돌아간 후 뱅글이의 바탕
ringcover = new THREE.Mesh(new THREE.PlaneGeometry(50, 15, 1), new THREE.MeshLambertMaterial({
    color: Math.random() * 0xffffff,
    opacity: 0,
    transparent: true
}));
ringcover.position.x = length + 1;
ringcover.rotation.y = Math.PI / 2;
group.add(ringcover);

ring = new THREE.Mesh(new THREE.RingGeometry(4.3, 5.55, 32), new THREE.MeshBasicMaterial({
    color: ringcolor,       // 뱅글이가 다 돌아간 후에 나오는 원의 색
    transparent: true,
    opacity: 0
}));
ring.position.x = length + 1.1;
ring.rotation.y = Math.PI / 2;
group.add(ring);

// fake shadow
(function () {
    var plain, i;
    for (i = 0; i < 10; i++) {
        plain = new THREE.Mesh(new THREE.PlaneGeometry(length * 2 + 1, radius * 3, 1), new THREE.MeshBasicMaterial({
            color: 0x000000, // 이상한 애 ...
            transparent: true,
            opacity: 0
        }));
        plain.position.z = -2.5 + i * 0.5;
        group.add(plain);
    }
})();

renderer = new THREE.WebGLRenderer({
    antialias: true,
    transparent: true,
    alpha: true
});
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(canvassize, canvassize);
renderer.setClearColor(0x000000, 0);        // 캔버스의 바탕화면 색
$wrap.appendChild(renderer.domElement);

$body.addEventListener('mousedown', start, false);
$body.addEventListener('touchstart', start, false);
$body.addEventListener('mouseup', back, false);
$body.addEventListener('touchend', back, false);

animate();


function start() {
    toend = true;
}

function back() {
    toend = false;
}

function tilt(percent) {
    group.rotation.y = percent * 0.5;
}

var maxstep = 192;

function render() {

    var progress;

    animatestep = Math.max(0, Math.min(240, toend ? animatestep + 1 : animatestep - 4));
    acceleration = easing(animatestep, 0, 1, 240);

    if (acceleration > 0.35) {
        progress = (acceleration - 0.35) / 0.65;
        group.rotation.y = -Math.PI / 2 * progress;
        group.position.z = 50 * progress;
        progress = Math.max(0, (acceleration - 0.97) / 0.03);
        mesh.material.opacity = 1 - progress;
        ringcover.material.opacity = ring.material.opacity = progress;
        ring.scale.x = ring.scale.y = 0.9 + 0.1 * progress;
    }

    renderer.render(scene, camera);
    if (animatestep >= maxstep) {
        animatestep = maxstep;
        // toDo : 여기서 사용자가 사진 올렸는지, 올린 사진으로부터 추출한 얼굴이 있는지 확인하고, 다른 페이지를 로드한다.
        if (true) {
            $(location).attr('href', 'http://127.0.0.1:8000/your_nickname')

        }
    }
}

function animate() {
    mesh.rotation.x += rotatevalue + acceleration;
    render();
    requestAnimationFrame(animate);
}

function easing(t, b, c, d) {
    if ((t /= d / 2) < 1) return c / 2 * t * t + b;
    return c / 2 * ((t -= 2) * t * t + 2) + b;
}
